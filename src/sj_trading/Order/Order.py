from abc import ABC, abstractmethod
from pydantic import BaseModel, ConfigDict, Field
import logging
import shioaji as sj
from shioaji.constant import *
from sj_trading.Utils.Order import *

class Order:
    # TODO: 應該有更好設計
    '''
    trade: 下單
    report: 回報
    '''
    def __init__(self, factId: int):
        self.trade = []
        self.report = []
        self.factId = factId
    
    def updateTrade(self, trade):
        self.trade.append(trade)
    
    def updateReport(self, report):
        self.report.append(report)
    
    def getId(self) -> str:
        if self.trade:
            return self.trade[-1].order.id
        return "-1"

class OrderFactBase(ABC):
    '''
    負責處理下單和回報/存中間所有Orders
    每個Strategy class持有Factory list
    Strategy呼叫onOrder (下單)
    OrderFactManager呼叫onReceive (回報)
    '''
    def setId(self, id: int):
        '''
        自編Order Factory Id
        由Factory Manager的addFact設定
        '''
        self.id = id
    
    def getId(self) -> int:
        return self.id
    
    @abstractmethod
    def onOrder(self, price=None):
        pass

    @abstractmethod
    def onReceive(self, rpt):
        pass
    
class OrderFactStock(OrderFactBase):
    # TODO
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def onOrder(self, action, price):
        pass
    def onReceive(self, rpt):
        pass
        
class OrderFactFutOpt(BaseModel, OrderFactBase):
    api: object
    quantity: int
    price_type: FuturesPriceType
    order_type: OrderType
    oc_type: FuturesOCType
    contract: object
    # orders: list[Order] = Field(default_factory=list)
    
    class Config:
        extra = "ignore"
    
    # def getOrder(self, id: str):
    #     return next((ord for ord in self.orders if ord.getId() == id), None)
    
    def onOrder(self, action, price):
        order = self.api.Order(
            action=action, 
            price=price,
            quantity=self.quantity, 
            price_type=self.price_type,
            order_type=self.order_type,
            octype=self.oc_type,
            account=self.api.futopt_account
        )
        trade = self.api.place_order(self.contract, order)
        newOrder = Order(self.id)
        newOrder.updateTrade(trade)
        # self.orders.append(newOrder)
        
        logging.INFO(f"New Order: {trade}")
    
    def onReceive(self, rpt):
        pass
    
        