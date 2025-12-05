import shioaji as sj
from collections import defaultdict, deque
from sj_trading.Strategy.BaseStrategy import BaseStrategy
from sj_trading.Utils.Kbar import *
from sj_trading.Utils.log import system_logger
from .data import ticks_data, kbars_data, ha_kbars_data

class QuotePublisher:
    def __init__(self, contracts: set):
        self.subscriber = defaultdict(dict)  # key: contract str.
        self.nextSubId = 0
        # every tick symbol has a kbar builder
        self.kbar_builders = {}

    def add_subscriber(self, st: BaseStrategy) -> int:
        for s in st.symbol:
            self.subscriber[s][self.nextSubId] = st
        self.nextSubId += 1
        return self.nextSubId - 1
        
    def remove_subscriber(self, id: int):
        for sub_d in self.subscriber.values():
            sub_d.pop(id, None)
    
    def notify_all(self, pause: bool):
        # 蒐集到完整k線數據才notify
        # 收到tick的symbol和原先註冊的不一致
        for symbol, data_q in ticks_data.items():
            if symbol not in self.kbar_builders:
                self.kbar_builders[symbol] = KBarBuilder()
            if data_q:
                front = data_q.popleft()  # thread-safe
                next_kbar = self.kbar_builders[symbol].update(front)
                
                if next_kbar:
                    system_logger.info(f'New Kbar data has been generated! {next_kbar}')

                    next_data = next_kbar
                    if kbars_data[symbol]:
                        next_ha_kbar = heikin_ashi(kbars_data[symbol][-1], next_kbar)
                        ha_kbars_data[symbol].append(next_ha_kbar)
                        
                    for sub in self.subscriber[symbol].values():
                        if sub.use_ha and kbars_data[symbol]:
                            next_data = next_ha_kbar 
                        sub.OnTick(next_data, pause=pause)
    
                    kbars_data[symbol].append(next_kbar)
                    