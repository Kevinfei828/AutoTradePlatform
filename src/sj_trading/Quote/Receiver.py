import shioaji as sj
import threading
from shioaji import TickFOPv1, Exchange
from sj_trading.Utils.log import *
from .data import ticks_data

class FuturesQuoteReceiver:
    def start_receive(self, api, contracts: set):
        api.set_context(ticks_data)   
        for contract in contracts:
            api.quote.subscribe(
                contract=contract,
                quote_type=sj.constant.QuoteType.Tick,
                version=sj.constant.QuoteVersion.v1,
            )

        # set_context參數綁定self
        @api.on_tick_fop_v1(bind=True)
        def quote_callback(self, exchange: Exchange, tick: TickFOPv1):
            # self為ticks_data
            self[tick.code].append(tick)  # thread-safe
            system_logger.info(f'Receive tick {tick.code} on thread {threading.get_native_id()}')
            
        
        
        

        

        
            
        

    
        
        
        