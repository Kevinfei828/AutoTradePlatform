import logging
from dataclasses import dataclass
from enum import Enum
from typing import Optional
from decimal import Decimal
from shioaji.constant import *
from sj_trading.Order.Order import OrderFactFutOpt
from sj_trading.Utils.Constant import PositionType
    

@dataclass
class Position:
    id: Optional[str] = None
    type: Optional[PositionType] = PositionType.EMPTY
    price: Optional[Decimal] = None
    size: Optional[int] = 0

def init_orderFact(config):
    match config["contract_type"]:
        case "Indexs":
            pass
        # case "Stocks":
        #     return OrderFactStock(**config)
        case "Futures":
            return OrderFactFutOpt(**config)
        case "Options":
            return OrderFactFutOpt(**config)
        case _:
            pass
    