import os

def load_backtest_config(dir: str):
    """
    讀取src/config/backtest下所有設定檔，檔名為xxx.cfg
    設定格式：key=value
    回傳 dict
    """
    if not os.path.exists(dir):
        return {}
    
    config = {}
    interval = None
    type = None
    strategy = None
    fund = 100000 # 預設資金10萬
    for file in os.listdir(dir):
        path = os.path.join(dir, file)
        if not os.path.isfile(path) or not file.lower().endswith(".cfg"):
            continue
    
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
            
                # 自動轉成 int
                if value.isdigit():
                    value = int(value)

                if key == "interval":
                    interval = value
                elif key == "type":
                    type = value
                elif key == "strategy":
                    strategy = value
                elif key == "fund":
                    fund = int(value)
                else:
                    config[key] = value
                    
    return config, interval, type, strategy, fund

def load_order_config(dir: str) -> list[dict]:
    """
    讀取src/config/order下所有設定檔，檔名為xxx.cfg
    設定格式：key=value
    """
    res = []
    if not os.path.exists(dir):
        return res
    
    for file in os.listdir(dir):
        path = os.path.join(dir, file)
        if not os.path.isfile(path) or not file.lower().endswith(".cfg"):
            continue 

        with open(path, "r", encoding="utf-8") as f:
            config = {}
            for line in f:
                line = line.strip()
                # 略過空白與註解
                if line == "" or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue

                key, value = line.split("=", 1)

                key = key.strip()
                value = value.strip()
            
                # 自動轉成 int
                if value.isdigit():
                    value = int(value)

                config[key] = value
            res.append(config)
                    
    return res