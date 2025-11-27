import shioaji as sj
import logging
import os
from datetime import date
from functools import partial
from dotenv import load_dotenv
from sj_trading.Quote import FuturesQuoteReceiver
from sj_trading.BackTest import BackTester
from sj_trading.Strategy import RangeFilter_1, RangeFilter_2
from sj_trading.Utils.Config import *
from sj_trading.Utils.Strategy import load_strategy, init_strategy, set_order_strategy
from sj_trading.Utils.logger import set_logger
from sj_trading.Order.Manager import OrderFactManager, OrderManager
from sj_trading.Utils.Contract import ContractResolver

def main():
    # TODO1: loop
    # TODO2: 回測/下單選項
    set_logger("src/log")
    load_dotenv()
    
    # 設定永豐API
    api = sj.Shioaji(simulation=True)
    api.login(
        api_key=os.environ["API_KEY"],
        secret_key=os.environ["SECRET_KEY"],
        subscribe_trade=True,  # 訂閱回報
        fetch_contract=True
    )
    api.activate_ca(
        ca_path=os.environ["CA_CERT_PATH"],
        ca_passwd=os.environ["CA_PASSWORD"],
    )
    logging.info(f"Login success!")
    logging.info(f"已獲取商品檔: {api.Contracts}")
    contract_resolver = ContractResolver(api)
    
    # 讀策略設定檔
    strategy_cfg = load_strategy("src/config/strategy")
    if not strategy_cfg:
        raise Exception("尚未設定任何策略!")
    
    # 初始化strategy class
    strategies = init_strategy("src/sj_trading/Strategy", strategy_cfg)

    # 讀下單設定檔, 初始化order class
    config = load_order_config("src/config/order")
    if not config:
        raise Exception("下單設定檔有誤!")
    
    # 初始化Managers, 綁回報callback
    ordMgr = OrderManager()
    ordFactMgr = OrderFactManager(ordMgr)
    api.set_order_callback(partial(OrderFactManager.onReceive, ordFactMgr))
    set_order_strategy(api, contract_resolver, config, strategies, ordFactMgr)
    
    # 讀回測設定檔
    config, interval, type, strategy, fund = load_backtest_config("src/config/backtest")
    if not config:
        raise Exception("回測設定檔有誤!")
    if config.get("symbol") is not None:
        match config["symbol"]:
            case "TXFR1":
                config.pop("symbol")
                config["contract"] = api.Contracts.Futures.TXF.TXFR1
            case "MXFR1":
                config.pop("symbol")
                config["contract"] = api.Contracts.Futures.MXF.MXFR1
            case _:
                raise Exception("找不到對應代號")

    if interval is None:
        # 未設定interval，則預設用1分k
        interval = "1T"
    if type is None:
        # 未設定type，則預設用k線
        type = "kbars"
    if strategy is None or strategy == "RF1":
        # 未設定strategy, 則預設用RangeFilter_1
        strategy = RangeFilter_1()
    elif strategy == "RF2":
        strategy = RangeFilter_2()
        
    

    #DEBUG
    print(
        f"Start backtesting with the following configs: {config}, \
        type={type}, \
        strategy={strategy.__class__.__name__}, \
        interval={interval}"
    )

    # 回測
    backTester = BackTester(api)
    if type == "kbars":
        backTester.SetKbars(**config)
        backTester.ToInterval(interval)
        backTester.RunKbarBacktest(strategy, fund)
    elif type == "ticks":
        # TODO
        pass