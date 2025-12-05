import pandas as pd
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional
from dataclasses import dataclass

@dataclass
class KBar:
    code: Optional[str] = None
    start_time: Optional[datetime] = None

    open: Optional[Decimal] = None
    high: Optional[Decimal] = None
    low: Optional[Decimal] = None
    close: Optional[Decimal] = None

    volume: Optional[int] = None
    amount: Optional[Decimal] = None
    
# 平均k
@dataclass
class HA_KBar:
    code: Optional[str] = None
    start_time: Optional[datetime] = None

    open: Optional[Decimal] = None
    high: Optional[Decimal] = None
    low: Optional[Decimal] = None
    close: Optional[Decimal] = None

    volume: Optional[int] = None
    amount: Optional[Decimal] = None

class KBarBuilder:
    def __init__(self, interval_seconds: int = 60):
        self.interval = timedelta(seconds=interval_seconds)
        self.current_kbar: KBar | None = None
        self.current_bucket_time: datetime | None = None

    def _floor_time(self, dt: datetime) -> datetime:
        """Floor datetime to k-bar bucket (e.g. 12:01:23 → 12:01:00)"""
        ts = int(dt.timestamp())
        floored = ts - (ts % int(self.interval.total_seconds()))
        return datetime.fromtimestamp(floored)

    def update(self, tick) -> KBar | None:
        """
        Input: 1 tick
        Output: Finished KBar when a new bar starts, otherwise None
        """

        price = tick.close
        vol = tick.volume
        amt = tick.amount
        code = tick.code
        t = tick.datetime

        bucket_time = self._floor_time(t)

        if self.current_kbar is None:
            self._start_new_bar(code, bucket_time, price, vol, amt)
            return None

        if bucket_time == self.current_bucket_time:
            kb = self.current_kbar
            kb.high = max(kb.high, price)
            kb.low = min(kb.low, price)
            kb.close = price
            kb.volume += vol
            kb.amount += amt
            return None

        finished_bar = self.current_kbar

        self._start_new_bar(code, bucket_time, price, vol, amt)

        return finished_bar

    def _start_new_bar(self, code, bucket_time, price, vol, amt):
        self.current_bucket_time = bucket_time
        self.current_kbar = KBar(
            code=code,
            start_time=bucket_time,
            open=price,
            high=price,
            low=price,
            close=price,
            volume=vol,
            amount=amt,
        )

def resample(src: pd.DataFrame, interval: str) -> pd.DataFrame:
    src = src.resample(interval).agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum",
        "Amount": "sum"
    })
    src = src.dropna()
    return src

def heikin_ashi(pk: KBar, ck: KBar):
    
    ha_close = (ck.open + ck.high + ck.low + ck.close) / Decimal(4)
    ha_open = (pk.open + pk.close) / Decimal(2)

    ha_high = max(ck.high, ha_open, ha_close)
    ha_low  = min(ck.low, ha_open, ha_close)

    return HA_KBar(
            code=ck.code,
            start_time=ck.start_time,
            open=ha_open,
            high=ha_high,
            low=ha_low,
            close=ha_close,
            volume=ck.volume,
            amount=ck.amount,
        )