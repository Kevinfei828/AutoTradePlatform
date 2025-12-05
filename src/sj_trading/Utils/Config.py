import os

def load_backtest_config(dir: str):
    '''
    讀取src/config/backtest下所有設定檔，檔名為xxx.cfg
    設定格式：key=value
    回傳 dict
    '''
    if not os.path.exists(dir):
        return {}
    
    config = {}
    for file in os.listdir(dir):
        path = os.path.join(dir, file)
        if not os.path.isfile(path) or not file.lower().endswith('.cfg'):
            continue
    
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line == '' or line.startswith('#'):
                    continue
                if '=' not in line:
                    continue

                key, value = line.split('=', 1)

                key = key.strip()
                value = value.strip()
            
                # 自動轉成 int
                if value.isdigit():
                    value = float(value)
                    
                config[key] = value
                    
    return config

def load_order_config(dir: str, exit_file: str) -> tuple[list[dict], set[str]]:
    '''
    讀取src/config/order下所有設定檔，檔名為xxx.cfg
    設定格式：key=value
    '''
    res = []
    exit_st = set()
    if not os.path.exists(dir):
        return res
    
    for file in os.listdir(dir):
        path = os.path.join(dir, file)
        if not os.path.isfile(path) or not file.lower().endswith('.cfg'):
            continue 

        with open(path, 'r', encoding='utf-8') as f:
            if file.split('.', 1)[0].lower() == exit_file:
                for line in f:
                    line = line.strip()
                    if line == '' or line.startswith('#'):
                        continue
                    exit_st.add(line.lower())
            else:
                config = {}
                for line in f:
                    line = line.strip()
                    # 略過空白與註解
                    if line == '' or line.startswith('#'):
                        continue
                    if '=' not in line:
                        continue

                    key, value = line.split('=', 1)

                    key = key.strip()
                    value = value.strip()
                
                    # 自動轉成 int
                    if value.isdigit():
                        value = int(value)

                    config[key] = value
                res.append(config)
                    
    return res, exit_st