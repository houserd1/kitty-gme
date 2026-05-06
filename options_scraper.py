"""
options_scraper.py — Free-tier options data for the Kitty Score.

Pulls a daily snapshot of GME options from yfinance (call volume, put volume,
30-day ATM implied volatility) and computes derived metrics by comparing the
snapshot to history that the main script accumulates over time.

Limitations of free options data:
  - yfinance returns only a current snapshot, not a historical chain. The
    20-day call volume average and the 252-day IV range have to be built up
    from prior runs of this script. Until enough history accumulates, the
    derived metrics return None and the score's Layer 3 sits at zero for
    those signals (graceful degradation by design).
  - Bid/ask quality on options can be stale outside market hours.
  - yfinance is unofficial and rate-limited. Failures here are caught and
    return None rather than crashing the run.

Not financial advice.
"""

from __future__ import annotations

import math
from datetime import date, datetime
from typing import Optional


def _safe_float(x) -> Optional[float]:
    try:
        f = float(x)
        if math.isnan(f) or math.isinf(f):
            return None
        return f
    except (TypeError, ValueError):
        return None


def pull_snapshot(ticker: str = 'GME') -> dict:
    """
    Pull today's options snapshot from yfinance.

    Returns a dict with:
      call_volume: total call volume across all expiries (int or None)
      put_volume: total put volume across all expiries (int or None)
      put_call_ratio: put / call (float or None)
      atm_iv_30d: ATM implied vol on the expiry closest to 30 days out
      data_quality: short string describing what worked or failed
    """
    out = {
        'call_volume': None,
        'put_volume': None,
        'put_call_ratio': None,
        'atm_iv_30d': None,
        'data_quality': 'unknown',
    }

    try:
        import yfinance as yf
    except ImportError:
        out['data_quality'] = 'yfinance not installed'
        return out

    try:
        tk = yf.Ticker(ticker)
        expiries = tk.options
        if not expiries:
            out['data_quality'] = 'no expiries returned'
            return out

        # Current price for ATM strike pick.
        spot = None
        try:
            hist = tk.history(period='5d', auto_adjust=False)
            if len(hist) > 0:
                spot = _safe_float(hist['Close'].iloc[-1])
        except Exception:
            spot = None

        total_call_vol = 0
        total_put_vol = 0
        atm_iv_30d = None
        atm_iv_distance_days = None

        today = date.today()

        for exp_str in expiries:
            try:
                exp_date = datetime.strptime(exp_str, '%Y-%m-%d').date()
            except ValueError:
                continue

            try:
                chain = tk.option_chain(exp_str)
            except Exception:
                continue

            calls = chain.calls
            puts = chain.puts

            if calls is not None and 'volume' in calls.columns:
                cv = calls['volume'].fillna(0).sum()
                total_call_vol += int(cv)

            if puts is not None and 'volume' in puts.columns:
                pv = puts['volume'].fillna(0).sum()
                total_put_vol += int(pv)

            # Pick the contract closest to 30 days out at the strike closest to spot.
            if spot is not None and calls is not None and len(calls) > 0:
                days_out = (exp_date - today).days
                if days_out <= 0:
                    continue

                this_distance = abs(days_out - 30)
                if atm_iv_distance_days is None or this_distance < atm_iv_distance_days:
                    if 'strike' in calls.columns and 'impliedVolatility' in calls.columns:
                        idx = (calls['strike'] - spot).abs().idxmin()
                        iv = _safe_float(calls.loc[idx, 'impliedVolatility'])
                        if iv is not None and iv > 0:
                            atm_iv_30d = iv
                            atm_iv_distance_days = this_distance

        out['call_volume'] = total_call_vol if total_call_vol > 0 else None
        out['put_volume'] = total_put_vol if total_put_vol > 0 else None
        if total_call_vol > 0:
            out['put_call_ratio'] = total_put_vol / total_call_vol
        out['atm_iv_30d'] = atm_iv_30d

        if out['call_volume'] is None and out['atm_iv_30d'] is None:
            out['data_quality'] = 'snapshot empty'
        elif out['atm_iv_30d'] is None:
            out['data_quality'] = 'volume only, no IV'
        elif out['call_volume'] is None:
            out['data_quality'] = 'IV only, no volume'
        else:
            out['data_quality'] = 'ok'

        return out

    except Exception as e:
        out['data_quality'] = f'snapshot error: {type(e).__name__}'
        return out


def compute_relative(snapshot: dict, history: list) -> dict:
    """
    Given today's snapshot and the rolling history list, compute relative
    metrics that need history to be meaningful.

    Returns a dict with:
      call_ratio: today's call volume / 20-day average (or None)
      iv_rank: position of today's IV in the trailing range, 0-100 (or None)
      options_persistent: True if today plus the last 2 prior days all had
        call_ratio > 2x (or False if not, None if can't be computed)
      data_quality: short string
    """
    out = {
        'call_ratio': None,
        'iv_rank': None,
        'options_persistent': False,
        'data_quality': '',
    }

    if not snapshot or snapshot.get('call_volume') is None:
        out['data_quality'] = 'no snapshot'
        return out

    # 20-day call volume average from history.
    recent_call_vols = [
        e.get('call_volume') for e in history[-20:]
        if isinstance(e.get('call_volume'), (int, float)) and e.get('call_volume') > 0
    ]
    days_of_history = len(recent_call_vols)

    if days_of_history >= 5:
        avg = sum(recent_call_vols) / days_of_history
        if avg > 0:
            out['call_ratio'] = snapshot['call_volume'] / avg
        if days_of_history < 20:
            out['data_quality'] = f'partial: {days_of_history}/20 days'
        else:
            out['data_quality'] = 'ok'
    else:
        out['data_quality'] = f'awaiting history ({days_of_history}/20 days)'

    # IV rank from trailing IV range (up to 252 days).
    snap_iv = snapshot.get('atm_iv_30d')
    recent_ivs = [
        e.get('atm_iv_30d') for e in history[-252:]
        if isinstance(e.get('atm_iv_30d'), (int, float)) and e.get('atm_iv_30d') > 0
    ]
    if snap_iv is not None and len(recent_ivs) >= 30:
        iv_min = min(recent_ivs)
        iv_max = max(recent_ivs)
        if iv_max > iv_min:
            out['iv_rank'] = (snap_iv - iv_min) / (iv_max - iv_min) * 100.0

    # Persistence: today plus the last 2 prior days all had call_ratio > 2.
    if out['call_ratio'] is not None and out['call_ratio'] > 2.0:
        prior_ratios = [
            e.get('call_ratio') for e in history[-2:]
            if isinstance(e.get('call_ratio'), (int, float))
        ]
        if len(prior_ratios) == 2 and all(r > 2.0 for r in prior_ratios):
            out['options_persistent'] = True

    return out
