import pandas as pd
import numpy as np

def true_range(high, low, prev_close):
    if prev_close is None:
        return high - low
    return max(high - low, abs(high - prev_close), abs(low - prev_close))

def sma(values):
    if not values:
        return None
    return sum(values) / len(values)

def rma(input: pd.Series, length: int) -> pd.Series:
    alpha = 1 / length
    return input.ewm(alpha=alpha, min_periods=length, adjust=False).mean()

# def atr_rma(length: int = 14) -> pd.Series:
#     return rma(tr(), length)

def ema(data: np.array, span: int):
    alpha = 2 / (span + 1)
    ema = np.zeros_like(data, dtype=float)
    ema[0] = data[0]
    for i in range(1, len(data)):
        ema[i] = alpha * data[i] + (1 - alpha) * ema[i - 1]
    return ema

def smooth_range(period: int, mult: float, closes: np.ndarray):
    if len(closes) < period + 2:
        return np.nan

    x = closes
    diff = np.abs(np.diff(x))
    # 使用 numpy 的 EMA 實作
    avrng = ema(diff, period)
    wper = period * 2 - 1
    smrng = ema(avrng, wper) * mult
    return smrng[-1]