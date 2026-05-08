"""
technicals.py — Advanced technical indicators added in Kitty v1.1.

Computes signals Gill referenced directly in his streams: On-Balance Volume
trend (the headline addition), MACD bullish crossover proximity, and a
weekly RSI(14) confirmation. All three operate on the daily DataFrame the
main script already pulls from yfinance, so there is no second network
call.

Graceful degradation: each computation returns None when the input is
short or contains gaps that would produce a misleading result. The score
just doesn't earn those points and the data_quality block notes the gap.

Not financial advice.
"""

from __future__ import annotations

import math
from typing import Optional


def _is_finite(x) -> bool:
    try:
        v = float(x)
        return not (math.isnan(v) or math.isinf(v))
    except (TypeError, ValueError):
        return False


def compute_obv_slope(close, volume, window: int = 20) -> Optional[float]:
    """Compute the slope of On-Balance Volume over the trailing window.

    OBV is the running sum of signed volume: + on up days, - on down days,
    0 on flat. The slope of the trailing 20 entries (linear regression)
    captures whether accumulation or distribution dominated.

    Returns the slope (positive means accumulation pattern) or None if
    there is not enough data.
    """
    try:
        import numpy as np
    except ImportError:
        return None

    if close is None or volume is None or len(close) < window + 1:
        return None

    delta = close.diff()
    direction = delta.copy()
    direction[delta > 0] = 1
    direction[delta < 0] = -1
    direction[delta == 0] = 0
    direction = direction.fillna(0)

    obv = (direction * volume).cumsum()
    recent = obv.iloc[-window:].dropna()
    if len(recent) < window:
        return None

    x = np.arange(len(recent), dtype=float)
    y = recent.to_numpy(dtype=float)
    if not all(_is_finite(v) for v in y):
        return None

    try:
        slope, _intercept = np.polyfit(x, y, 1)
    except Exception:
        return None

    return float(slope) if _is_finite(slope) else None


def compute_macd_crossover_recent(
    close,
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
    window: int = 10,
) -> Optional[bool]:
    """True if a bullish MACD crossover happened in the last `window` bars.

    Standard MACD parameters (12, 26, 9). A bullish crossover is the bar
    where the MACD line moves from below the signal line to above it.
    """
    if close is None or len(close) < slow + signal + window:
        return None

    try:
        ema_fast = close.ewm(span=fast, adjust=False).mean()
        ema_slow = close.ewm(span=slow, adjust=False).mean()
        macd = ema_fast - ema_slow
        sig = macd.ewm(span=signal, adjust=False).mean()
        crossovers = (macd.shift(1) < sig.shift(1)) & (macd > sig)
        recent = crossovers.iloc[-window:]
        return bool(recent.any())
    except Exception:
        return None


def compute_weekly_rsi(close, period: int = 14) -> Optional[float]:
    """Weekly RSI(14) from daily closes, resampled to Friday weekly bars.

    Confirms the trend on a slower timeframe than the daily RSI. The
    score rewards a value in the 40-65 recovery / uptrend zone.
    """
    if close is None or len(close) < period * 7 + 7:
        return None

    try:
        weekly = close.resample('W-FRI').last().dropna()
    except Exception:
        return None

    if len(weekly) < period + 1:
        return None

    try:
        delta = weekly.diff()
        gain = delta.where(delta > 0, 0).rolling(period).mean()
        loss = -delta.where(delta < 0, 0).rolling(period).mean()
        last_gain = float(gain.iloc[-1])
        last_loss = float(loss.iloc[-1])
        if not _is_finite(last_gain) or not _is_finite(last_loss):
            return None
        if last_loss == 0:
            return 100.0 if last_gain > 0 else 50.0
        rs = last_gain / last_loss
        rsi = 100 - (100 / (1 + rs))
        return float(rsi) if _is_finite(rsi) else None
    except Exception:
        return None


def compute_advanced(history_df) -> tuple[dict, str]:
    """Bundle the three v1.1 Layer 2 signals from a yfinance daily DataFrame.

    Returns a tuple of (results_dict, status_string). The dict carries:
        obv_slope: float | None
        obv_slope_positive: bool | None
        macd_bullish_recent: bool | None
        weekly_rsi: float | None
    """
    out = {
        'obv_slope': None,
        'obv_slope_positive': None,
        'macd_bullish_recent': None,
        'weekly_rsi': None,
    }
    if history_df is None or len(history_df) == 0:
        return out, 'no data'

    try:
        close = history_df['Close']
        volume = history_df['Volume']
    except Exception as e:
        return out, f'{type(e).__name__}: {e}'

    out['obv_slope'] = compute_obv_slope(close, volume)
    if out['obv_slope'] is not None:
        out['obv_slope_positive'] = out['obv_slope'] > 0

    out['macd_bullish_recent'] = compute_macd_crossover_recent(close)
    out['weekly_rsi'] = compute_weekly_rsi(close)

    gaps = [k for k in ('obv_slope', 'macd_bullish_recent', 'weekly_rsi') if out[k] is None]
    if gaps:
        return out, f'partial: missing {",".join(gaps)}'
    return out, 'ok'
