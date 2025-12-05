import time
import shioaji as sj
from datetime import datetime, date
from sj_trading.Utils.Futures import *

# def st_subscribe_quote(recver: QuoteReceiver, strategies, contracts: list[str]):
#     for st in strategies:
#         recver.add_subscriber(st)
#     for c in contracts:
#         recver.start_receive(c)

def is_clear_day(d: date):
        # 結算日 (每月第三個星期三日盤)
        if date.weekday() != 2:  # 2 = Wednesday
            return False

        # The third Wednesday must fall between 15th and 21st
        return 15 <= d.day <= 21
    
def str_to_time(t: str):
    h, m, s = map(int, t.split(':'))
    return time(h, m, s)

def is_normal_time(d: date, t: time) -> bool:
    adjust_close = ft_normal['clear'] if is_clear_day(d) else ft_normal['close']
    return str_to_time(ft_normal['open']) <= t <= str_to_time(adjust_close)

def is_after_time(d: date, t: time) -> bool:
    return t >= str_to_time(ft_after['open']) or t <= str_to_time(ft_after['close'])

def ticks_to_kbars_pandas(df):
    """
    df: DataFrame with columns ["time", "close"]
    time must be a datetime64[ns]
    """
    df = df.set_index("time")

    kbars = df["close"].resample("1T").agg(
        open="first",
        high="max",
        low="min",
        close="last"
    ).dropna()

    return kbars.reset_index()

def recover_intra_data(api, contract):
    '''
    回補邏輯: 由系統啟動時間往前回補當天日/夜盤，如系統啟動時為收盤則不回補
    '''
    now_time = str_to_time(datetime.now().strftime("%H:%M:%S"))
    now_date = date.today()
    if is_normal_time(now_date, now_time):
        time_start = ft_normal['open']
    elif is_after_time(now_date, now_time):
        time_start = ft_after['open']
    else:
        return None
 
    recoverd_ticks = api.ticks(
        contract=contract, 
        date=now_date,
        query_type=sj.constant.TicksQueryType.RangeTime,
        time_start=time_start,
        time_end=now_time,
    )
    return recoverd_ticks