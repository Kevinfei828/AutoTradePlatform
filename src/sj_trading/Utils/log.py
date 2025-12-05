import logging
import os
from datetime import date

# logging.debug(f"現在價格={price} trend={trend}")
# logging.info("策略開始執行")
# logging.warning("資料異常")
# logging.error(f"出現錯誤: {err}")
    
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
LOG_PATH_SYS = "src/log/system"
LOG_PATH_BACKTEST = "src/log/backtest"
LOG_PATH_ORDER = "src/log/order"

def set_logger(name: str, path: str, level=logging.INFO):
    os.makedirs(path, exist_ok=True)
    formatted_date = date.today().strftime("%Y%m%d")
    formatted_path = os.path.join(path, formatted_date + ".log")
    with open(formatted_path, 'a') as f:
        pass

    handler = logging.FileHandler(formatted_path)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    
    return logger

system_logger = set_logger("system_logger", LOG_PATH_SYS)
backtest_logger = set_logger("backtest_logger", LOG_PATH_BACKTEST)
order_logger = set_logger("order_logger", LOG_PATH_ORDER)
