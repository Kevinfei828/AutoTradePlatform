import logging
import os
from datetime import date

# logging.debug(f"現在價格={price} trend={trend}")
# logging.info("策略開始執行")
# logging.warning("資料異常")
# logging.error(f"出現錯誤: {err}")

def set_logger(path: str):
    os.makedirs(path, exist_ok=True)
    formatted_date = date.today().strftime("%Y%m%d")
    formatted_path = os.path.join(path, formatted_date + ".log")
    with open(formatted_path, 'a') as f:
        pass
    
    logging.basicConfig(
        level=logging.INFO,
        # level=logging.DEBUG
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(formatted_path, encoding="utf-8"),
        ]
    )