import os
import importlib
from sj_trading.Utils.Order import init_orderFact
from sj_trading.Utils.Contract import ContractResolver
from sj_trading.Utils.log import system_logger
from sj_trading.Utils.Constant import *
from sj_trading.Order.Order import OrderFactManager

def load_st_ct(
    dir: str,
    resolver: ContractResolver,
    exit_cfg: set[str]
) -> tuple[set[str], set[str], dict[str, dict]]:
    ct_name = set()
    sts_name = set()
    res_cfg = {}
    if not os.path.exists(dir):
        os.makedirs(dir)
        return ct_name, res_cfg
    
    for file in os.listdir(dir):
        path = os.path.join(dir, file)
        if not os.path.isfile(path) or not file.endswith('.cfg'):
            continue
        
        ret = {}
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line == '' or line.startswith('#'):
                    continue
                if '=' not in line:
                    continue
                
                key, value = line.split('=', 1)
                key = key.strip().lower()
                value = value.strip().lower()
                
                if value == 'true':
                    value = True
                elif value == 'false':
                    value = False
                # parse symbol != all的st cfg
                elif key == 'symbol':
                    if value != 'all':
                        s = set()
                        ct_name.add(value.upper())
                        s.add(value)
                        value = s
                    else:
                        continue
                elif key == 'exit':
                    if value not in exit_cfg:
                        continue
                elif value.isdigit():
                    value = int(value)
                else:
                    try:
                        value = float(value)
                    except ValueError:
                        print(f'Incorrect strategy configs: {key}, {value}')
                
                ret[key] = value
        st_name = file.split('.', 1)[0]
        res_cfg[st_name] = ret
        sts_name.add(st_name)

    return ct_name, sts_name, res_cfg

def init_strategy(
    dir: str,
    sts: set[str],
    st_cfgs: dict[str, dict],
    contracts: set[str],
) -> list:
    # 依st_cfgs初始化所有sts中的策略
    if not os.path.exists(dir):
        os.makedirs(dir)
        return []

    ord_res = []
    for st in sts:
        cfg = st_cfgs[st]
        path = os.path.join(dir, st + '.py')
        if not (os.path.exists(path) and os.path.isfile(path)):
            continue
            
        module_name = f'{PACKAGE}.{st}'
        module = importlib.import_module(module_name)
        
        if not hasattr(module, st):
            continue

        ord_cls = getattr(module, st, None)
        # parse symbol = 'all'
        if 'symbol' not in cfg:
            cfg['symbol'] = contracts
        try:
            if ord_cls:
                print(f'cfg: {cfg}')
                ord_inst = ord_cls(**cfg)
        except TypeError as e:
            print(e)
            continue

        ord_res.append(ord_inst)
    
    return ord_res

def set_order_strategy(
    api,
    resolver: ContractResolver, 
    config: list[dict], 
    strategies: list, 
    ordMgr: OrderFactManager,
):
    st_dict = {}
    for st in strategies:
        st_dict[type(st).__name__] = st
    for cfg in config:
        cfg['api'] = api
        cfg['contract'] = resolver.resolve(cfg['contract'])        
        if cfg['strategy'] == 'All':
            for inst in st_dict.values():
                orderFact = init_orderFact(cfg)
                ordMgr.initFact(api, orderFact)
                inst.setCurrOrderFact(orderFact)
        else:
            orderFact = init_orderFact(cfg)
            ordMgr.initFact(api, orderFact)
            st_dict.get(cfg['strategy']).setCurrOrderFact(orderFact)
            
        
        
