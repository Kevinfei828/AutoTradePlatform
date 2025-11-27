import os
import importlib
from sj_trading.Utils.Order import init_orderFact
from sj_trading.Utils.Contract import ContractResolver

NAMEKEY = "name"
PACKAGE = "sj_trading.Strategy"
def load_strategy(dir: str) -> list[dict]:
    res = []
    if not os.path.exists(dir):
        os.makedirs(dir)
        return res
    
    for file in os.listdir(dir):
        path = os.path.join(dir, file)
        if not os.path.isfile(path) or not file.endswith(".cfg"):
            continue
        
        ret = {}
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line == "" or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue
                
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
            
                if value.isdigit():
                    value = int(value)
                elif value.lower() == "True":
                    value = True
                elif value.lower() == "False":
                    value = False
                else:
                    try:
                        value = float(value)
                    except ValueError:
                        pass
                
                ret[key] = value
        ret[NAMEKEY] = file.split(".", 1)[0]
        res.append(ret)

    return res

def init_strategy(dir: str, strategies: list[dict]) -> list:
    # 有設定檔且正確設定class name才初始化
    res = []
    if not os.path.exists(dir):
        os.makedirs(dir)
        return res
    
    for cfg in strategies:
        path = os.path.join(dir, cfg[NAMEKEY] + ".py")
        if not (os.path.exists(path) and os.path.isfile(path)):
            continue
            
        module_name = f"{PACKAGE}.{cfg[NAMEKEY]}"
        module = importlib.import_module(module_name)
        
        if not hasattr(module, cfg[NAMEKEY]):
            continue

        cls = getattr(module, cfg[NAMEKEY])
        params = {k: v for k, v in cfg.items() if k != NAMEKEY}

        try:
            inst = cls(**params)
        except TypeError as e:
            print(f"[ERROR] Init {cfg[NAMEKEY]} failed: {e}")
            continue
        
        res.append(inst)
    return res

def set_order_strategy(api, resolver: ContractResolver, config: list[dict], strategies: list, ordMgr):
    st_dict = {}
    for st in strategies:
        st_dict[type(st).__name__] = st
    for cfg in config:
        cfg["api"] = api
        cfg["contract"] = resolver.resolve(cfg["contract"])
        orderFact = init_orderFact(cfg)
        if cfg["strategy"] == "All":
            for inst in st_dict.values():
                inst.addOrderFact(orderFact)
        else:
            st_dict.get(cfg["strategy"]).addOrderFact(orderFact)
        ordMgr.addFact(orderFact)
        
