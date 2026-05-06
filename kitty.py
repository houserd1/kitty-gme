#!/usr/bin/env python3
"""
kitty.py — Daily Kitty Score computation for GME.

Pulls free public data (yfinance, SEC EDGAR, NYSE Reg SHO list), reads
manual flags from manual_flags.json (Gill / Cohen activity, fundamentals
that change quarterly), computes the five-layer Kitty Score, writes
data.json for the dashboard, appends to history.json, and pushes a debrief
via ntfy.sh.

Designed to run unattended in GitHub Actions on a weekday cron. Every data
pull is wrapped in try/except so a single source going down does not crash
the run; the affected layer just scores zero and the data_quality block
notes the gap.

Not financial advice. The Kitty Score reports condition similarity to
historical pre-spike setups, not predictions.
"""

from __future__ import annotations

import argparse
import base64
import json
import math
import os
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

try:
    import yfinance as yf
    import requests
except ImportError:
    print("Missing dependencies. Run: pip install -r requirements.txt")
    sys.exit(1)

import options_scraper

# --- CONFIG ---------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent
DATA_FILE = REPO_ROOT / 'data.json'
HISTORY_FILE = REPO_ROOT / 'history.json'
MANUAL_FLAGS_FILE = REPO_ROOT / 'manual_flags.json'

NTFY_TOPIC = os.environ.get('NTFY_TOPIC', '').strip()
NTFY_SERVER = os.environ.get('NTFY_SERVER', 'https://ntfy.sh')

DEFAULT_ALERT_THRESHOLD = 51
HISTORY_LIMIT = 365


# --- DATA PULLS -----------------------------------------------------------

def pull_gme_data() -> tuple[dict, str]:
    """Pull GME daily data from yfinance and compute technicals.

    Returns (data_dict, status_string). data_dict is empty on failure.
    """
    try:
        gme = yf.Ticker('GME')
        hist = gme.history(period='1y', auto_adjust=False)
        if len(hist) < 50:
            return {}, f'insufficient history ({len(hist)} rows)'

        last = hist.iloc[-1]
        close = float(last['Close'])
        vol = float(last['Volume'])

        ma50 = float(hist['Close'].tail(50).mean())
        ma200 = float(hist['Close'].tail(200).mean()) if len(hist) >= 200 else None
        avg_vol_20 = float(hist['Volume'].tail(20).mean())

        delta = hist['Close'].diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = -delta.where(delta < 0, 0).rolling(14).mean()
        rsi = 50.0
        try:
            last_gain = float(gain.iloc[-1])
            last_loss = float(loss.iloc[-1])
            if last_loss > 0 and not math.isnan(last_gain):
                rs = last_gain / last_loss
                rsi_calc = 100 - (100 / (1 + rs))
                if not math.isnan(rsi_calc) and not math.isinf(rsi_calc):
                    rsi = float(rsi_calc)
            elif last_loss == 0 and last_gain > 0:
                rsi = 100.0
        except Exception:
            rsi = 50.0

        vol_ratio = vol / avg_vol_20 if avg_vol_20 > 0 else 1.0
        if math.isnan(vol_ratio) or math.isinf(vol_ratio):
            vol_ratio = 1.0

        return {
            'price': close,
            'price_over_50dma': close > ma50,
            'price_over_200dma': bool(ma200 is not None and close > ma200),
            'rsi': rsi,
            'vol_ratio': vol_ratio,
            'ma50': ma50,
            'ma200': ma200,
        }, 'ok'
    except Exception as e:
        return {}, f'{type(e).__name__}: {e}'


def check_xrt_threshold() -> tuple[bool | None, str]:
    """Check NYSE Reg SHO threshold list for XRT.

    Returns (status, message). status is True/False if known, None if check failed.
    """
    today = date.today().strftime('%Y%m%d')
    url = f'https://www.nyse.com/api/regulatory/threshold-securities/download?selectedDate={today}'
    try:
        r = requests.get(url, timeout=15, headers={'User-Agent': 'KittyMonitor/2.0'})
        if r.status_code == 200 and r.text:
            return ('XRT' in r.text.upper()), 'ok'
        return None, f'http {r.status_code}'
    except Exception as e:
        return None, f'{type(e).__name__}: {e}'


def check_recent_form4_filings() -> tuple[bool | None, str]:
    """Check SEC EDGAR for recent GameStop Form 4 filings (insider transactions)."""
    url = 'https://data.sec.gov/submissions/CIK0001326380.json'
    try:
        r = requests.get(
            url,
            timeout=15,
            headers={'User-Agent': 'KittyMonitor research-only'},
        )
        if r.status_code != 200:
            return None, f'http {r.status_code}'
        data = r.json()
        recent = data.get('filings', {}).get('recent', {})
        forms = recent.get('form', [])
        dates = recent.get('filingDate', [])
        cutoff = date.today() - timedelta(days=7)
        for form, fdate_str in zip(forms, dates):
            if form == '4':
                fdate = datetime.strptime(fdate_str, '%Y-%m-%d').date()
                if fdate >= cutoff:
                    return True, 'ok'
        return False, 'ok'
    except Exception as e:
        return None, f'{type(e).__name__}: {e}'


def days_to_quarter_end() -> int:
    today = date.today()
    candidates = [
        date(today.year, 3, 31),
        date(today.year, 6, 30),
        date(today.year, 9, 30),
        date(today.year, 12, 31),
        date(today.year + 1, 3, 31),
    ]
    upcoming = [q for q in candidates if q >= today]
    return (upcoming[0] - today).days


def days_to_earnings() -> tuple[int | None, str]:
    """Pull next earnings date via yfinance. Returns (days, status).

    yfinance has changed the calendar return shape between versions
    (sometimes dict, sometimes DataFrame). This handles both.
    """
    try:
        gme = yf.Ticker('GME')
        cal = gme.calendar
        if cal is None:
            return None, 'no calendar'

        ed = None
        if isinstance(cal, dict):
            ed = cal.get('Earnings Date')
        elif hasattr(cal, 'columns') and 'Earnings Date' in getattr(cal, 'columns', []):
            try:
                ed = cal['Earnings Date'].iloc[0]
            except Exception:
                ed = None
        elif hasattr(cal, 'get'):
            try:
                ed = cal.get('Earnings Date')
            except Exception:
                ed = None

        if isinstance(ed, list) and ed:
            ed = ed[0]
        if ed is None:
            return None, 'no earnings date'
        if hasattr(ed, 'date'):
            ed = ed.date()
        if not isinstance(ed, date):
            return None, f'unexpected type {type(ed).__name__}'
        return (ed - date.today()).days, 'ok'
    except Exception as e:
        return None, f'{type(e).__name__}: {e}'


# --- SCORING --------------------------------------------------------------

def compute_score(inputs: dict) -> dict:
    l1 = 0
    if inputs.get('cash_tier') == 'over50':
        l1 += 10
    elif inputs.get('cash_tier') == 'over30':
        l1 += 5
    if inputs.get('ocf_positive'):
        l1 += 5
    if inputs.get('no_dilution_risk'):
        l1 += 5

    l2 = 0
    if inputs.get('price_over_50dma'):
        l2 += 5
    if inputs.get('price_over_200dma'):
        l2 += 5
    rsi = inputs.get('rsi', 50)
    if 40 <= rsi <= 65:
        l2 += 5
    if rsi > 75:
        l2 -= 5
    if inputs.get('vol_ratio', 1.0) > 1.5:
        l2 += 5

    l3 = 0
    cr = inputs.get('call_ratio')
    if cr is not None:
        if cr > 3:
            l3 += 15
        elif cr > 2:
            l3 += 10
    iv = inputs.get('iv_rank')
    if iv is not None:
        if iv < 15:
            l3 += 10
        elif iv < 30:
            l3 += 5
    pcr = inputs.get('put_call_ratio')
    if pcr is not None and pcr < 0.5:
        l3 += 5
    if inputs.get('options_persistent'):
        l3 += 5

    l4 = 0
    if inputs.get('xrt_threshold'):
        l4 += 5
    if inputs.get('days_to_quarter_end', 60) < 15:
        l4 += 3
    if inputs.get('short_vol_pct', 45) > 50:
        l4 += 3
    if inputs.get('borrow_fee_rising'):
        l4 += 2
    if inputs.get('drs_locked', True):
        l4 += 2

    l5 = 0
    if inputs.get('cohen_buy_7d'):
        l5 += 5
    if inputs.get('cohen_post_7d'):
        l5 += 3
    if inputs.get('gill_active_7d'):
        l5 += 10
    e_days = inputs.get('days_to_earnings')
    if e_days is not None and 0 <= e_days <= 30:
        l5 += 3
    if inputs.get('macro_event'):
        l5 += 2

    return {
        'l1': l1, 'l2': l2, 'l3': l3, 'l4': l4, 'l5': l5,
        'total': l1 + l2 + l3 + l4 + l5,
    }


def state_label(score: int) -> str:
    if score >= 86:
        return 'Significant Convergence'
    if score >= 71:
        return 'Heightened'
    if score >= 51:
        return 'Elevated'
    if score >= 31:
        return 'Watching'
    return 'Quiet'


def state_emoji(score: int) -> str:
    if score >= 71:
        return '🔴'
    if score >= 51:
        return '🟡'
    if score >= 31:
        return '🟢'
    return '⚪'


# --- DEBRIEF GENERATION ---------------------------------------------------

def generate_debrief(scores: dict, inputs: dict, data_quality: dict) -> str:
    state = state_label(scores['total'])
    lines = [
        f"Kitty Score {scores['total']}/100 — {state}",
        f"Floor {scores['l1']}/20 · Tech {scores['l2']}/20 · Tape {scores['l3']}/25 "
        f"· Struct {scores['l4']}/15 · Cat {scores['l5']}/20",
    ]

    if inputs.get('price') is not None:
        rsi = inputs.get('rsi', 0)
        vr = inputs.get('vol_ratio', 0)
        lines.append(f"Price ${inputs['price']:.2f} · RSI {rsi:.0f} · Vol {vr:.2f}x")

    notes = []
    if scores['l3'] >= 20:
        notes.append("Options tape is loud.")
    if inputs.get('gill_active_7d'):
        notes.append("Gill recently active. Strongest single-day catalyst on record.")
    if inputs.get('cohen_buy_7d'):
        notes.append("Cohen Form 4 buy in the last 7 days.")
    if scores['l4'] >= 10 and inputs.get('xrt_threshold'):
        notes.append("Structural backdrop loaded with XRT on threshold.")
    if inputs.get('rsi', 50) > 75:
        notes.append("RSI overbought. Late cycle, not pre-spike.")
    if scores['total'] >= 71:
        notes.append("Setup matches late-stage pre-spike conditions of late April 2024.")

    cr = inputs.get('call_ratio')
    iv = inputs.get('iv_rank')
    if cr is not None and cr > 2 and iv is not None and iv < 30:
        notes.append("Cheap convex calls available. The asymmetric setup Gill targets.")

    if notes:
        lines.append('')
        lines.extend(f"• {n}" for n in notes)

    gaps = [k for k, v in data_quality.items() if v not in ('ok', None) and 'awaiting' in str(v).lower()]
    failed = [k for k, v in data_quality.items() if v not in ('ok', None) and 'awaiting' not in str(v).lower()]
    if gaps:
        lines.append('')
        lines.append(f"Awaiting: {', '.join(gaps)}")
    if failed:
        lines.append(f"Data gaps: {', '.join(failed)}")

    return '\n'.join(lines)


def what_changes_it(scores: dict, inputs: dict) -> list[str]:
    items = []
    cr = inputs.get('call_ratio')
    iv = inputs.get('iv_rank')
    if scores['l3'] < 15:
        cr_str = f"{cr:.2f}x" if cr is not None else "unknown"
        iv_str = f"{iv:.0f}" if iv is not None else "unknown"
        items.append(f"Call volume ratio above 2x with IV rank under 30 (now {cr_str}, IV rank {iv_str})")
    if not inputs.get('gill_active_7d'):
        items.append("Gill posting on X, Reddit, or YouTube")
    if not inputs.get('cohen_buy_7d'):
        items.append("A new Form 4 disclosing Cohen open-market buying")
    if not inputs.get('xrt_threshold'):
        items.append("XRT appearing on the Reg SHO threshold list")
    dq = inputs.get('days_to_quarter_end', 60)
    if dq > 20:
        items.append(f"Approach of quarter-end (now {dq} days out)")
    if not inputs.get('options_persistent'):
        items.append("Three or more consecutive days of unusual options activity")
    return items[:5]


# --- I/O ------------------------------------------------------------------

def load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception as e:
        print(f"warn: failed to parse {path.name}: {e}", file=sys.stderr)
        return default


def _sanitize(obj):
    """Recursively replace NaN/inf with None so downstream JSON parsers behave."""
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    if isinstance(obj, dict):
        return {k: _sanitize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_sanitize(v) for v in obj]
    return obj


def save_json(path: Path, obj):
    safe = _sanitize(obj)
    path.write_text(json.dumps(safe, indent=2, default=str, allow_nan=False), encoding='utf-8')


def append_history(history: list, entry: dict) -> list:
    today_str = entry['date']
    history = [h for h in history if h.get('date') != today_str]
    history.append(entry)
    history.sort(key=lambda h: h.get('date', ''))
    return history[-HISTORY_LIMIT:]


# --- NOTIFICATIONS --------------------------------------------------------

def push_notification(title: str, body: str, priority: str = 'default') -> tuple[bool, str]:
    """Push a message via ntfy.sh.

    ntfy headers technically require ASCII. Non-ASCII titles are encoded
    via RFC 2047 base64. The body itself is sent as raw UTF-8 bytes.
    """
    if not NTFY_TOPIC:
        return False, 'NTFY_TOPIC not set'

    headers = {
        'Priority': priority,
        'Tags': 'cat',
    }

    if any(ord(c) > 127 for c in title):
        b64 = base64.b64encode(title.encode('utf-8')).decode('ascii')
        headers['Title'] = f'=?UTF-8?B?{b64}?='
    else:
        headers['Title'] = title

    try:
        r = requests.post(
            f'{NTFY_SERVER}/{NTFY_TOPIC}',
            data=body.encode('utf-8'),
            headers=headers,
            timeout=15,
        )
        if r.status_code == 200:
            return True, 'ok'
        return False, f'http {r.status_code}: {r.text[:120]}'
    except Exception as e:
        return False, f'{type(e).__name__}: {e}'


# --- MAIN -----------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='Kitty GME Daily Monitor')
    parser.add_argument('--alert-threshold', type=int, default=DEFAULT_ALERT_THRESHOLD,
                        help=f'Push only if score at or above this (default {DEFAULT_ALERT_THRESHOLD})')
    parser.add_argument('--always-push', action='store_true',
                        help='Push every run regardless of score')
    parser.add_argument('--no-push', action='store_true',
                        help='Skip the push entirely')
    parser.add_argument('--dry-run', action='store_true',
                        help='Print only, do not write data.json or history.json or push')
    args = parser.parse_args()

    print(f"=== Kitty Run — {date.today().isoformat()} ===")

    flags = load_json(MANUAL_FLAGS_FILE, {})
    history = load_json(HISTORY_FILE, [])
    if not isinstance(history, list):
        history = []

    print("Pulling GME price/technicals...")
    gme_data, gme_status = pull_gme_data()
    print(f"  -> {gme_status}")

    print("Pulling options snapshot...")
    snap = options_scraper.pull_snapshot('GME')
    print(f"  -> {snap.get('data_quality')}")

    print("Computing options relative metrics...")
    rel = options_scraper.compute_relative(snap, history)
    print(f"  -> {rel.get('data_quality')}")

    print("Checking XRT Reg SHO threshold list...")
    xrt_status, xrt_msg = check_xrt_threshold()
    print(f"  -> {xrt_msg}")

    print("Checking SEC EDGAR for recent Form 4...")
    cohen_buy, edgar_msg = check_recent_form4_filings()
    print(f"  -> {edgar_msg}")

    print("Pulling earnings calendar...")
    e_days, earnings_msg = days_to_earnings()
    print(f"  -> {earnings_msg}")

    inputs = {
        'price': gme_data.get('price'),
        'rsi': gme_data.get('rsi', 50),
        'vol_ratio': gme_data.get('vol_ratio', 1.0),
        'ma50': gme_data.get('ma50'),
        'ma200': gme_data.get('ma200'),
        'price_over_50dma': gme_data.get('price_over_50dma', False),
        'price_over_200dma': gme_data.get('price_over_200dma', False),

        'call_volume': snap.get('call_volume'),
        'put_volume': snap.get('put_volume'),
        'atm_iv_30d': snap.get('atm_iv_30d'),
        'call_ratio': rel.get('call_ratio'),
        'iv_rank': rel.get('iv_rank'),
        'put_call_ratio': snap.get('put_call_ratio'),
        'options_persistent': rel.get('options_persistent', False),

        'xrt_threshold': xrt_status if xrt_status is not None else False,
        'days_to_quarter_end': days_to_quarter_end(),
        'short_vol_pct': flags.get('short_vol_pct', 45),
        'borrow_fee_rising': bool(flags.get('borrow_fee_rising', False)),
        'drs_locked': bool(flags.get('drs_locked', True)),

        'cohen_buy_7d': cohen_buy if cohen_buy is not None else False,
        'cohen_post_7d': bool(flags.get('cohen_post_7d', False)),
        'gill_active_7d': bool(flags.get('gill_active_7d', False)),
        'days_to_earnings': e_days,
        'macro_event': bool(flags.get('macro_event', False)),

        'cash_tier': flags.get('cash_tier', 'over50'),
        'ocf_positive': bool(flags.get('ocf_positive', True)),
        'no_dilution_risk': bool(flags.get('no_dilution_risk', True)),
    }

    scores = compute_score(inputs)
    state = state_label(scores['total'])

    data_quality = {
        'price_data': gme_status,
        'options_data': snap.get('data_quality'),
        'options_relative': rel.get('data_quality'),
        'xrt_threshold': xrt_msg,
        'edgar_form4': edgar_msg,
        'earnings_calendar': earnings_msg,
    }

    debrief = generate_debrief(scores, inputs, data_quality)
    changes = what_changes_it(scores, inputs)

    print()
    print(debrief)
    print()

    repo = os.environ.get('GITHUB_REPOSITORY', '').strip()
    repo_url = f"https://github.com/{repo}" if repo else None

    record = {
        'date': date.today().isoformat(),
        'updated_at': datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'score': scores,
        'state': state,
        'inputs': inputs,
        'debrief': debrief,
        'what_changes': changes,
        'manual_flags': flags,
        'data_quality': data_quality,
        'alert_threshold': args.alert_threshold,
        'repo_url': repo_url,
    }

    history_entry = {
        'date': record['date'],
        'total': scores['total'],
        'l1': scores['l1'], 'l2': scores['l2'], 'l3': scores['l3'],
        'l4': scores['l4'], 'l5': scores['l5'],
        'price': inputs.get('price'),
        'rsi': inputs.get('rsi'),
        'vol_ratio': inputs.get('vol_ratio'),
        'call_volume': inputs.get('call_volume'),
        'put_volume': inputs.get('put_volume'),
        'atm_iv_30d': inputs.get('atm_iv_30d'),
        'call_ratio': inputs.get('call_ratio'),
        'iv_rank': inputs.get('iv_rank'),
        'xrt_threshold': inputs.get('xrt_threshold'),
        'cohen_buy_7d': inputs.get('cohen_buy_7d'),
        'gill_active_7d': inputs.get('gill_active_7d'),
        'state': state,
    }

    if args.dry_run:
        print("(dry run) skipping data.json, history.json, and push")
        return 0

    save_json(DATA_FILE, record)
    history = append_history(history, history_entry)
    save_json(HISTORY_FILE, history)
    print(f"Wrote {DATA_FILE.name} and updated {HISTORY_FILE.name} ({len(history)} entries)")

    should_push = (not args.no_push) and (args.always_push or scores['total'] >= args.alert_threshold)
    if should_push:
        title = f"{state_emoji(scores['total'])} GME Kitty {scores['total']}/100 · {state}"
        ok, msg = push_notification(title, debrief)
        print(f"Push: {'sent' if ok else 'failed'} ({msg})")
    else:
        print("Push skipped.")

    return 0


if __name__ == '__main__':
    sys.exit(main())
