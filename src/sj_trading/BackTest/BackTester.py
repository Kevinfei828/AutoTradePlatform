from shioaji.data import Ticks, Kbars
from sj_trading.Utils import Kbar
from sj_trading.Strategy import BaseStrategy
from sj_trading.Utils.Plot import plotSignal, plotTrend
import pandas as pd

# class Ticks(BaseModel):
#     ts: typing.List[int]
#     close: typing.List[float]
#     volume: typing.List[int]
#     bid_price: typing.List[float]
#     bid_volume: typing.List[int]
#     ask_price: typing.List[float]
#     ask_volume: typing.List[int]
#     tick_type: typing.List[int]

# class Kbars(BaseModel):
#     ts: typing.List[int]
#     Open: typing.List[float]
#     High: typing.List[float]
#     Low: typing.List[float]
#     Close: typing.List[float]
#     Volume: typing.List[int]
#     Amount: typing.List[float]
    
class BackTester:
    '''
    給定Strategy做backtest，用API初始化
    '''
    def __init__(self, api):
        self.api = api
        self.kbars = None
        self.ticks = None
        self.signals = []
        self.trends = []
        
    def SetKbars(self, *args, **kwargs):
        self.kbars = self.api.kbars(*args, **kwargs)
    
    def SetTicks(self, *args, **kwargs):
        self.ticks = self.api.ticks(*args, **kwargs)
    
    def ToInterval(self, interval: str):
        if self.ticks is not None:
            self.ticks = pd.DataFrame({**self.ticks})
            self.ticks.ts = pd.to_datetime(self.ticks.ts)
            # TODO: ticks resample
            
        if self.kbars is not None:
            self.kbars = pd.DataFrame({**self.kbars})
            self.kbars.ts = pd.to_datetime(self.kbars.ts)
            self.kbars = self.kbars.set_index("ts")
            self.kbars = Kbar.resample(self.kbars, interval)
        
    def RunKbarBacktest(
        self, strategy: BaseStrategy, fund: int,
        excel_name="signals.xlsx", fig_name="signals.png"
    ):
        if self.kbars is None:
            raise ValueError("kbars is not set. Call SetKbars() first.")
        
        # DEBUG
        print(self.kbars)
        print(f"---start backtesting, rows = {len(self.kbars)} ---")

        for ts, row in self.kbars.iterrows():
            high = row["High"]
            low = row["Low"]
            close = row["Close"]

            res = strategy.OnTick(high, low, close)
            if "signal" in res:
                self.signals.append({
                    "ts": ts,
                    "signal": res["signal"],
                    "close": close,
                })
            if "trend" in res:
                self.trends.append({
                    "ts": ts,
                    "up": res["up"],
                    "dn": res["dn"],
                })
                
        sig_df = pd.DataFrame(self.signals)
        trend_df = pd.DataFrame(self.trends)
        
        plotSignal(self.kbars, sig_df)
        plotTrend(self.kbars, trend_df)

        return sig_df

    def StartTicksBT(self, strategy):
        # TODO
        pass
        

