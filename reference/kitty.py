#!/usr/bin/env python3
"""
kitty.py — Scheduled Kitty Score computation and push notifications for GME.

Designed to be run daily via cron. Pulls free public data (yfinance, SEC EDGAR,
NYSE threshold list), accepts manual overrides for inputs that can't be
auto-pulled (Gill activity, options unusual activity flag), computes the
Kitty Score, and pushes a debrief notification.

Usage:
    Auto-run with all defaults:
        python kitty.py
    With manual flags for what auto-pull can't see:
        python kitty.py --gill-active --options-persistent --cohen-buy
    With config file:
        python kitty.py --config kitty_config.yaml

Cron example (runs every weekday at 5pm ET):
    0 17 * * 1-5 cd /path/to/kitty && /usr/bin/python3 kitty.py >> kitty.log 2>&1

Requirements:
    pip install yfinance requests python-dateutil

Notification setup (ntfy.sh, free):
    1. Visit ntfy.sh on your phone, install the app
    2. Subscribe to a topic, e.g. "kitty-gme-{random-suffix}"
    3. Set NTFY_TOPIC below or pass via env var
"""

import argparse
import json
import os
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

try:
    import yfinance as yf
    import requests
except ImportError:
    print("Missing deps. Run: pip install yfinance requests python-dateutil")
    sys.exit(1)

# --- CONFIG ---------------------------------------------------------------

NTFY_TOPIC = os.environ.get('NTFY_TOPIC', 'kitty-gme-CHANGE-ME-PLEASE')
NTFY_SERVER = os.environ.get('NTFY_SERVER', 'https://ntfy.sh')
HISTORY_FILE = Path.home() / '.kitty_history.json'

# --- DATA PULLS -----------------------------------------------------------

def pull_gme_data():
    """Pull GME daily data from yfinance and compute technicals."""
    try:
        gme = yf.Ticker('GME')
        hist = gme.history(period='1y', auto_adjust=False)
        if len(hist) < 200:
            return None
        
        last = hist.iloc[-1]
        close = float(last['Close'])
        vol = float(last['Volume'])
        
        ma50 = float(hist['Close'].tail(50).mean())
        ma200 = float(hist['Close'].tail(200).mean())
        avg_vol_20 = float(hist['Volume'].tail(20).mean())
        
        # RSI(14)
        delta = hist['Close'].diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = -delta.where(delta < 0, 0).rolling(14).mean()
        rs = gain / loss
        rsi = float(100 - (100 / (1 + rs.iloc[-1])))
        
        return {
            'price': close,
            'price_over_50dma': close > ma50,
            'price_over_200dma': close > ma200,
            'rsi': rsi,
            'vol_ratio': vol / avg_vol_20 if avg_vol_20 > 0 else 1.0,
            'ma50': ma50,
            'ma200': ma200,
        }
    except Exception as e:
        print(f"GME data pull failed: {e}")
        return None


def check_xrt_threshold():
    """
    Check NYSE Reg SHO threshold list for XRT.
    The NYSE publishes daily as a downloadable file.
    """
    try:
        # NYSE publishes daily at this URL pattern
        today = date.today().strftime('%Y%m%d')
        url = f'https://www.nyse.com/api/regulatory/threshold-securities/download?selectedDate={today}'
        r = requests.get(url, timeout=10, headers={'User-Agent': 'KittyMonitor/1.0'})
        if r.status_code == 200:
            return 'XRT' in r.text.upper()
        return None  # Unknown
    except Exception as e:
        print(f"XRT threshold check failed: {e}")
        return None


def check_recent_cohen_filings():
    """
    Check SEC EDGAR for recent GameStop Form 4 filings (insider transactions).
    Returns True if any Form 4 filed in last 7 days.
    """
    try:
        # GameStop CIK is 0001326380
        url = 'https://data.sec.gov/submissions/CIK0001326380.json'
        r = requests.get(url, timeout=10, headers={'User-Agent': 'KittyMonitor research@example.com'})
        if r.status_code != 200:
            return None
        data = r.json()
        recent = data.get('filings', {}).get('recent', {})
        forms = recent.get('form', [])
        dates = recent.get('filingDate', [])
        cutoff = date.today() - timedelta(days=7)
        for form, fdate_str in zip(forms, dates):
            if form == '4':
                fdate = datetime.strptime(fdate_str, '%Y-%m-%d').date()
                if fdate >= cutoff:
                    return True
        return False
    except Exception as e:
        print(f"EDGAR check failed: {e}")
        return None


def days_to_quarter_end():
    today = date.today()
    quarter_ends = [
        date(today.year, 3, 31),
        date(today.year, 6, 30),
        date(today.year, 9, 30),
        date(today.year, 12, 31),
    ]
    upcoming = [q for q in quarter_ends if q >= today]
    if not upcoming:
        return (date(today.year + 1, 3, 31) - today).days
    return (upcoming[0] - today).days


def days_to_earnings():
    """Pull earnings calendar from yfinance. Returns days, or None if unavailable."""
    try:
        gme = yf.Ticker('GME')
        cal = gme.calendar
        if cal is None or 'Earnings Date' not in cal:
            return None
        earnings_date = cal.get('Earnings Date')
        if isinstance(earnings_date, list) and len(earnings_date) > 0:
            ed = earnings_date[0]
            if hasattr(ed, 'date'):
                ed = ed.date()
            return (ed - date.today()).days
        return None
    except Exception:
        return None


# --- SCORING --------------------------------------------------------------

def compute_score(inputs):
    # Layer 1 - Fundamental Floor
    l1 = 0
    if inputs.get('cash_over_50_mcap'): l1 += 10
    elif inputs.get('cash_over_30_mcap'): l1 += 5
    if inputs.get('ocf_positive'): l1 += 5
    if inputs.get('no_dilution_risk'): l1 += 5
    
    # Layer 2 - Technical
    l2 = 0
    if inputs.get('price_over_50dma'): l2 += 5
    if inputs.get('price_over_200dma'): l2 += 5
    rsi = inputs.get('rsi', 50)
    if 40 <= rsi <= 65: l2 += 5
    if rsi > 75: l2 -= 5
    if inputs.get('vol_ratio', 1.0) > 1.5: l2 += 5
    
    # Layer 3 - Options Tape
    l3 = 0
    cr = inputs.get('call_ratio', 1.0)
    if cr > 3: l3 += 15
    elif cr > 2: l3 += 10
    iv = inputs.get('iv_rank', 50)
    if iv < 15: l3 += 10
    elif iv < 30: l3 += 5
    if inputs.get('put_call_ratio', 1.0) < 0.5: l3 += 5
    if inputs.get('options_persistent'): l3 += 5
    
    # Layer 4 - Structural
    l4 = 0
    if inputs.get('xrt_threshold'): l4 += 5
    if inputs.get('days_to_quarter_end', 60) < 15: l4 += 3
    if inputs.get('short_vol_pct', 45) > 50: l4 += 3
    if inputs.get('borrow_fee_rising'): l4 += 2
    if inputs.get('drs_locked', True): l4 += 2
    
    # Layer 5 - Catalyst
    l5 = 0
    if inputs.get('cohen_buy_7d'): l5 += 5
    if inputs.get('cohen_post_7d'): l5 += 3
    if inputs.get('gill_active_7d'): l5 += 10
    e_days = inputs.get('days_to_earnings')
    if e_days is not None and 0 <= e_days <= 30: l5 += 3
    if inputs.get('macro_event'): l5 += 2
    
    total = l1 + l2 + l3 + l4 + l5
    return {'l1': l1, 'l2': l2, 'l3': l3, 'l4': l4, 'l5': l5, 'total': total}


def state_label(score):
    if score >= 86: return 'Significant Convergence'
    if score >= 71: return 'Heightened'
    if score >= 51: return 'Elevated'
    if score >= 31: return 'Watching'
    return 'Quiet'


def state_emoji(score):
    if score >= 71: return '🔴'
    if score >= 51: return '🟡'
    if score >= 31: return '🟢'
    return '⚪'


# --- DEBRIEF GENERATION ---------------------------------------------------

def generate_debrief(scores, inputs):
    lines = []
    state = state_label(scores['total'])
    
    lines.append(f"Kitty Score: {scores['total']}/100 — {state}")
    lines.append(f"Floor:{scores['l1']}/20 Tech:{scores['l2']}/20 Tape:{scores['l3']}/25 Struct:{scores['l4']}/15 Cat:{scores['l5']}/20")
    
    if inputs.get('price'):
        lines.append(f"Price: ${inputs['price']:.2f}")
    
    notes = []
    if scores['l3'] >= 20:
        notes.append("Options tape is loud.")
    if inputs.get('gill_active_7d'):
        notes.append("Gill recently active — historically the strongest single catalyst.")
    if inputs.get('cohen_buy_7d'):
        notes.append("Cohen Form 4 buy in the last week.")
    if scores['l4'] >= 10 and inputs.get('xrt_threshold'):
        notes.append("Structural backdrop loaded with XRT on threshold.")
    if inputs.get('rsi', 50) > 75:
        notes.append("RSI overbought — late cycle, not pre-spike.")
    if scores['total'] >= 71:
        notes.append("Setup matches late-stage pre-spike conditions of late April 2024.")
    
    if notes:
        lines.append("")
        for n in notes:
            lines.append(f"• {n}")
    
    return "\n".join(lines)


# --- NOTIFICATIONS --------------------------------------------------------

def push_notification(title, body, priority='default', tags=None):
    """Push via ntfy.sh."""
    if NTFY_TOPIC == 'kitty-gme-CHANGE-ME-PLEASE':
        print("WARNING: NTFY_TOPIC not configured. Notification not sent.")
        return False
    
    headers = {
        'Title': title,
        'Priority': priority,
    }
    if tags:
        headers['Tags'] = ','.join(tags)
    
    try:
        r = requests.post(
            f'{NTFY_SERVER}/{NTFY_TOPIC}',
            data=body.encode('utf-8'),
            headers=headers,
            timeout=10,
        )
        return r.status_code == 200
    except Exception as e:
        print(f"Push failed: {e}")
        return False


# --- HISTORY --------------------------------------------------------------

def load_history():
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text())
        except Exception:
            return []
    return []


def save_history(entry):
    history = load_history()
    today_str = date.today().isoformat()
    history = [h for h in history if h.get('date') != today_str]
    history.append(entry)
    history = history[-365:]  # keep last year
    HISTORY_FILE.write_text(json.dumps(history, indent=2))


# --- MAIN -----------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='Kitty GME Daily Monitor')
    
    # Manual override flags for inputs that auto-pull can't see reliably
    parser.add_argument('--gill-active', action='store_true', help='Gill social media active in last 7d')
    parser.add_argument('--cohen-post', action='store_true', help='Cohen X post in last 7d')
    parser.add_argument('--options-persistent', action='store_true', help='3+ days of unusual options activity')
    parser.add_argument('--call-ratio', type=float, default=1.0, help='Call volume ratio vs 20d avg (manual)')
    parser.add_argument('--iv-rank', type=float, default=50, help='IV rank 0-100 (manual)')
    parser.add_argument('--put-call-ratio', type=float, default=1.0, help='Put/call volume ratio')
    parser.add_argument('--short-vol-pct', type=float, default=45, help='Short volume %% (manual)')
    parser.add_argument('--borrow-fee-rising', action='store_true', help='Borrow fee trending up week-over-week')
    parser.add_argument('--cash-tier', choices=['over50', 'over30', 'under30'], default='over50', 
                        help='Cash + securities vs market cap')
    parser.add_argument('--no-ocf-positive', action='store_true', help='Operating cash flow NOT positive')
    parser.add_argument('--dilution-risk', action='store_true', help='Imminent dilution announced')
    parser.add_argument('--no-drs-locked', action='store_true', help='DRS share count below ~25%%')
    parser.add_argument('--macro-event', action='store_true', help='Material macro/regulatory event')
    
    parser.add_argument('--alert-threshold', type=int, default=51, 
                        help='Push notification only if score at or above this (default 51)')
    parser.add_argument('--always-push', action='store_true', help='Always push notification')
    parser.add_argument('--dry-run', action='store_true', help='Print only, do not push or save')
    
    args = parser.parse_args()
    
    print(f"=== Kitty Run — {date.today().isoformat()} ===")
    
    # Auto-pull
    print("Pulling GME data...")
    gme_data = pull_gme_data() or {}
    print("Checking XRT threshold list...")
    xrt_status = check_xrt_threshold()
    print("Checking SEC EDGAR for recent Form 4...")
    cohen_buy = check_recent_cohen_filings()
    print("Checking earnings calendar...")
    e_days = days_to_earnings()
    
    # Assemble inputs
    inputs = {
        # Layer 1
        'cash_over_50_mcap': args.cash_tier == 'over50',
        'cash_over_30_mcap': args.cash_tier == 'over30',
        'ocf_positive': not args.no_ocf_positive,
        'no_dilution_risk': not args.dilution_risk,
        # Layer 2 (auto-pulled)
        'price': gme_data.get('price'),
        'price_over_50dma': gme_data.get('price_over_50dma', False),
        'price_over_200dma': gme_data.get('price_over_200dma', False),
        'rsi': gme_data.get('rsi', 50),
        'vol_ratio': gme_data.get('vol_ratio', 1.0),
        # Layer 3 (mostly manual - good options data is paywalled)
        'call_ratio': args.call_ratio,
        'iv_rank': args.iv_rank,
        'put_call_ratio': args.put_call_ratio,
        'options_persistent': args.options_persistent,
        # Layer 4
        'xrt_threshold': xrt_status if xrt_status is not None else False,
        'days_to_quarter_end': days_to_quarter_end(),
        'short_vol_pct': args.short_vol_pct,
        'borrow_fee_rising': args.borrow_fee_rising,
        'drs_locked': not args.no_drs_locked,
        # Layer 5
        'cohen_buy_7d': cohen_buy if cohen_buy is not None else False,
        'cohen_post_7d': args.cohen_post,
        'gill_active_7d': args.gill_active,
        'days_to_earnings': e_days,
        'macro_event': args.macro_event,
    }
    
    scores = compute_score(inputs)
    debrief = generate_debrief(scores, inputs)
    
    print()
    print(debrief)
    print()
    
    # Push if threshold met
    should_push = args.always_push or scores['total'] >= args.alert_threshold
    if should_push and not args.dry_run:
        emoji = state_emoji(scores['total'])
        title = f"{emoji} GME Kitty {scores['total']}/100 — {state_label(scores['total'])}"
        ok = push_notification(title, debrief)
        print(f"Push: {'sent' if ok else 'failed/skipped'}")
    elif args.dry_run:
        print("Dry run — no push, no save.")
    else:
        print(f"Score below alert threshold ({args.alert_threshold}). No push.")
    
    # Save history
    if not args.dry_run:
        entry = {
            'date': date.today().isoformat(),
            'total': scores['total'],
            **{f'l{i}': scores[f'l{i}'] for i in range(1, 6)},
            'price': inputs.get('price'),
            'rsi': inputs.get('rsi'),
            'vol_ratio': inputs.get('vol_ratio'),
            'xrt_threshold': inputs.get('xrt_threshold'),
            'cohen_buy_7d': inputs.get('cohen_buy_7d'),
            'gill_active_7d': inputs.get('gill_active_7d'),
        }
        save_history(entry)
        print(f"Saved to {HISTORY_FILE}")


if __name__ == '__main__':
    main()
