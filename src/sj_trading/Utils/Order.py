import logging
from dataclasses import dataclass
from enum import Enum
from shioaji.constant import *
from sj_trading.Order.Order import OrderFactFutOpt, OrderFactStock

# class Price(Enum):
#     LMT = 0
#     MKT = 1
#     MKP = 2
    
# class Order(Enum):
#     ROD = 0
#     IOC = 1
#     FOK = 2

# class OC(Enum):
#     Auto = 0
#     New = 1
#     Cover = 2
#     DayTrade = 3
    
def init_orderFact(config):
    match config["contract_type"]:
        case "Indexs":
            pass
        case "Stocks":
            return OrderFactStock(**config)
        case "Futures":
            return OrderFactFutOpt(**config)
        case "Options":
            return OrderFactFutOpt(**config)
        case _:
            pass
    