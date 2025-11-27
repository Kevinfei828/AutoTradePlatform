import pandas as pd

def resample(src: pd.DataFrame, interval: str) -> pd.DataFrame:
    src = src.resample(interval).agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum",
        "Amount": "sum"
    })
    src = src.dropna()
    return src