import shioaji as sj
import logging
import os
import threading
import time
from multiprocessing import Process, Pool
from datetime import date
from dotenv import load_dotenv
from sj_trading.BackTest.main import run_backtest
from sj_trading.Utils.Config import *
from sj_trading.Utils.Strategy import load_st_ct, init_strategy, set_order_strategy
from sj_trading.Utils.log import set_logger
from sj_trading.Utils.Contract import ContractResolver
from sj_trading.Event.Handler import EventHandler
from sj_trading.Utils.log import system_logger
from sj_trading.Event.io import start_io
from sj_trading.Quote.main import run_quote_receiver
from sj_trading.Report.main import run_report
from sj_trading.Strategy.main import run_strategy
from sj_trading.Quote.Publisher import QuotePublisher
from sj_trading.Utils.Constant import *

def main():
    load_dotenv()
    # io_thread = threading.Thread(target=start_io, args=(shutdown_io_event))
    # io_thread.start()
    
    # 系統內部events
    pause_event = threading.Event()
    end_event = threading.Event()
    shutdown_io_event = threading.Event()
    
    # 設定永豐API
    api = sj.Shioaji(simulation=True)
    api.login(
        api_key=os.environ['API_KEY'],
        secret_key=os.environ['SECRET_KEY'],
        subscribe_trade=True,  # 訂閱回報
        fetch_contract=True
    )
    api.activate_ca(
        ca_path=os.environ['CA_CERT_PATH'],
        ca_passwd=os.environ['CA_PASSWORD'],
    )
    system_logger.info(f'Login success!')
    
    # 系統外部events
    event_handler = EventHandler(api)
    event_handler.quote_event.wait()
    event_handler.quote_event.clear()
    system_logger.info(f'Fetch Contracts: {api.Contracts}')
    
    contract_resolver = ContractResolver(api)
    
    # 讀下單設定檔
    ord_cfg, exit_cfg = load_order_config(CFG_PATH_ORDER, EXIT_FILE)
    if not (ord_cfg and exit_cfg):
        print('尚未設定下單參數!')
    print(ord_cfg)
    print(exit_cfg)
    # 讀策略設定檔
    contracts, strategies, strategy_cfg = load_st_ct(CFG_PATH_STRATEGY, contract_resolver, exit_cfg)
    if not strategies:
        print('尚未設定策略參數!')
    
    print(strategy_cfg)

    st_inst = init_strategy(MAIN_PATH_STRATEGY, strategies, strategy_cfg, contracts)
    st_name = [type(inst).__name__ for inst in st_inst]
    print(f'Initialize order instances: {st_name}')
    
    print(contracts)

    run_quote_receiver(api, contracts, contract_resolver)
    event_handler.quote_event.wait()
    event_handler.quote_event.clear()
    
    # 初始化Managers, 綁回報callback
    ordMgr, ordFactMgr = run_report(api, contract_resolver, ord_cfg, st_inst)
    publisher = QuotePublisher(contracts) 

    main_str = '>> '
    usage = '''Usage:
    [Backtest]
    1. start Backtest: bt
    [Autotrade]
    1. start/resume Autotrade: at or autotrade
    2. pause Autotrade: p or p at or p autotrade
    3. list all orders: l or l order
    [System]
    1. exit program: e or exit or ctrl-D (Linux) or ctrl-Z (Windows)
    '''
    system_logger.info(f'Fetch contracts: {contracts}')
    print(usage)
    
    strategy_thread = threading.Thread(
        target=run_strategy,
        args=(end_event, pause_event, st_inst, publisher),
        daemon=True
    )

    while (1):
        user_input = input(main_str)
        match user_input.lower():
            case 'bt' | 'backtest':
                # TODO
                bt_config = load_backtest_config(CFG_PATH_BACKTEST)
                print(strategy_cfg)
                # contracts, strategies, strategy_cfg = load_st_ct(CFG_PATH_STRATEGY)
                backtest_thread = threading.Thread(
                    target=run_backtest,
                    args=(
                        api,
                        bt_config,
                        contract_resolver,
                        strategy_cfg,
                    )
                )
                backtest_thread.start()
                backtest_thread.join()
            case 'at' | 'autotrade':
                pause_event.clear()
                strategy_thread.start()
            case 'p' | 'p at' | 'p autotrade':
                pause_event.set()
            case 'e' | 'exit':
                # join系統內所有thread
                end_event.set()
                if strategy_thread and strategy_thread.is_alive():
                    strategy_thread.join()
                exit(0)
            case 'l' | 'l order':
                api.list_trades()
            case _:
                print(usage)
    
if __name__ == '__main__':
    main()