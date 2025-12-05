import shioaji as sj
import threading
from functools import partial
from sj_trading.Utils.Strategy import set_order_strategy
from sj_trading.Utils.Contract import ContractResolver
from sj_trading.Strategy import *
from sj_trading.Order.Order import *

def run_report(
    api,
    contract_resolver: ContractResolver,
    ord_cfg: list[dict],
    st_inst: list[BaseStrategy],
):
    ordMgr = OrderManager()
    ordFactMgr = OrderFactManager(ordMgr)
    set_order_strategy(api, contract_resolver, ord_cfg, st_inst, ordFactMgr)
    
    api.set_order_callback(partial(OrderFactManager.onReceive, ordFactMgr))
    return ordMgr, ordFactMgr