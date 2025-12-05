from abc import ABC, abstractmethod
from pydantic import BaseModel, ConfigDict, Field
import logging
import shioaji as sj
from shioaji.constant import *
from sj_trading.Utils.log import order_logger
from sj_trading.Report.Report import FuturesOrdRpt
from sj_trading.Report.DealReport import FuturesOrdDealRpt
from sj_trading.Utils.Constant import OrderClassType

class Order:
    '''
    一個Order object只會是下單或回報object
    '''
    def __init__(self, factId: int):
        self.type: OrderClassType = None
        self.content = None
        self.factId = factId

class OrderManager:
    '''
    整個系統應只初始化一個
    初始化順序為Factory->Order Manager
    管理所有Orders
    '''
    def __init__(self):
        self.orders = {}  # {order_id: str, list[Order]}
        self.factorders = {} # {fact_id: int, list[Order]}
    
    def getOrd_by_factId(self, factids: list[int]) -> list[Order]:
        ret = []
        for fact in factids:
            ret += self.factorders[fact]
        return ret
        
class OrderFactManager:
    '''
    整個系統應只初始化一個
    管理對應種類Order Factories，包含已委託/已成交
    根據factories分配callback
    '''
    def __init__(self, ordMgr: OrderManager):
        self.ids = 0
        self.ordMgr = ordMgr
        self.orderFacts = []
    
    def initFact(self, api, ordFact):
        # 初始化order factory的base part
        ordFact.id = self.ids
        ordFact.factmanager = self
        ordFact.api = api
        self.ids += 1
        self.orderFacts.append(ordFact)
    
    def onReceive(self, stat, msg):
        '''
        收回報callback: 參考永豐API格式
        '''
        order_logger.info(f'Receive {stat} Report')
        if 'trade_id' in msg:
            # 成交
            ordId = msg['trade_id']
            rpt = FuturesOrdDealRpt(**msg)
            ord_type = OrderClassType.RESPONSE_DEAL
        else:
            # 委託
            ordId = msg['order']['id']
            rpt = FuturesOrdRpt(**msg)
            ord_type = OrderClassType.RESPONSE_ORDER
        
        orig_ordlist = self.ordMgr.orders[ordId]
        orig_factid = orig_ordlist[0].factId
        rpt_ord = Order(orig_factid)
        rpt_ord.content = rpt
        rpt_ord.type = ord_type
        orig_ordlist.append(rpt_ord)

class OrderFactBase(ABC):
    '''
    負責處理下單和回報/存中間所有Orders
    每個Strategy class持有Factory list
    Strategy呼叫onOrder (下單)
    OrderFactManager呼叫onReceive (回報)
    '''
    def __init__(self):
        # 目前由Factory Manager初始化此部分
        self.id: int = None
        self.factmanager: OrderFactManager = None,
        self.api = None,
    
    @abstractmethod
    def getOrder(self, ord_id: str):
        pass
    
    @abstractmethod
    def onOrder(self, price=None):
        pass

# class OrderFactStock(OrderFactBase):
#     # TODO
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#     def onOrder(self, action, price):
#         pass
#     # def onReceive(self, rpt):
#     #     pass
        
class OrderFactFutOpt(OrderFactBase):
    def __init__(
        self,
        quantity: int,
        price_type: FuturesPriceType,
        order_type: OrderType,
        oc_type: FuturesOCType,
        contract: object,
        **kwargs,
    ):
        super().__init__()
        self.quantity = quantity
        self.price_type = price_type
        self.order_type = order_type 
        self.oc_type = oc_type
        self.contract = contract
        
    def getOrder(self, ord_id: str):
        # 回傳Order list中最新的Order
        ord_list = self.factmanager.ordMgr.orders[ord_id]
        if ord_list:
            return ord_list[-1]
    
    # TODO: 如order有單獨thread，則onOrder(..., OrderFactBase)
    def onOrder(self, action, price) -> Order:
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
        newOrder.type = OrderClassType.TRADE
        newOrder.content = trade
        self.factmanager.ordMgr.orders[trade.order.id] = newOrder
        self.factmanager.ordMgr.factorders[self.id] = newOrder

        order_logger.info(f"New Order: {trade}")
        return newOrder
