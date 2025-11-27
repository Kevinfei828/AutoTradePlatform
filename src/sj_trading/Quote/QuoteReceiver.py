import shioaji as sj
from collections import defaultdict, deque
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from shioaji import TickFOPv1, Exchange
from .QuoteType import future_dtype, day_max_len
from sj_trading.Strategy import BaseStrategy
import pandas as pd
import numpy as np

class QuoteReceiver(BaseModel, ABC):
    @abstractmethod
    def AddSubscriber(self, subscriber: BaseStrategy):
        pass
    
    @abstractmethod
    def RemoveSubScriber(self, subscriber: BaseStrategy):
        pass
    
    @abstractmethod
    def StartReceive(self, target: str):
        pass
        
class FuturesQuoteReceiver(QuoteReceiver):
    api: object
    subscriber: dict = Field(default_factory=dict)
    nextSubId: int = Field(default=0)

    def AddSubscriber(self, subscriber: BaseStrategy) -> int:
        self.subscriber[self.nextSubId] = subscriber
        self.nextSubId += 1
        return self.nextSubId - 1
        
    def RemoveSubScriber(self, index: int) -> None:
        self.subscriber.pop(index, None)
    
    def NotifySubscribers(self, tick: TickFOPv1) -> None:
        for sub in self.subscriber.values():
            res = sub.OnTick(tick)
            # TODO OnAfterTick: 根據OnTick結果決定是否下單
            # sub.OnAfterTick(res)
        
    def StartReceive(self, target: str):
        self.api.quote.subscribe(
            self.api.Contracts.Futures.MXF[target],
            quote_type = sj.constant.QuoteType.Tick,
            version = sj.constant.QuoteVersion.v1,
        )

        # set_context參數綁定self
        @self.api.on_tick_fop_v1()
        def quote_callback(exchange: Exchange, tick: TickFOPv1):
            # append quote to message queue
            # self[tick.code][self.idx]['open'] = tick.open
            # self[tick.code][self.idx]['close'] = tick.close
            # self[tick.code][self.idx]['high'] = tick.high
            # self[tick.code][self.idx]['low'] = tick.low
            # print(f"Exchange: {exchange}, Tick: {tick}")
            self.NotifySubscribers(tick)
            
        
        
        

        

        
            
        

    
        
        
        