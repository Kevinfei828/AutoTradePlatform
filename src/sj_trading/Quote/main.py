import threading
from collections import defaultdict, deque
from .Receiver import FuturesQuoteReceiver
from sj_trading.Utils.Contract import ContractResolver
from sj_trading.Utils.Strategy import load_st_ct
from sj_trading.Utils.Constant import *
from sj_trading.Utils.log import system_logger

def run_quote_receiver(
    api, 
    contracts: set[str],
    contract_resolver: ContractResolver,
):
    system_logger.info(f'Quote thread start with id: {threading.get_native_id()}')
    # TODO: 有可能callback進來時剛好切到其他thread嗎?
    ft_quote_receiver = FuturesQuoteReceiver()
    contracts = [contract_resolver.resolve(s) for s in contracts]
    # subscribe
    ft_quote_receiver.start_receive(api, contracts)
    print(f'Start receiving quote: {contracts}')
                
                