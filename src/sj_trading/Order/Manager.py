import logging
from sj_trading.Order.OrderReport import FuturesOrdRpt
from sj_trading.Order.OrderDealReport import FuturesOrdDealRpt

class OrderManager:
    '''
    整個系統應只初始化一個
    初始化順序為Factory->Order Manager
    管理所有Orders
    '''
    def __init__(self):
        self.orders = {}  # {order_id, order}
    
    def getOrd(self, orderId: str):
        return self.orders[orderId]
    
    # TODO
    def addOrd(self, order):
        self.orders[order["order"]["id"]] = order
    
class OrderFactManager:
    '''
    整個系統應只初始化一個
    管理對應種類Order Factories，包含已委託/已成交
    根據factories分配callback
    '''
    def __init__(self, ordMgr):
        self.ids = 0
        self.ordMgr = ordMgr
        self.orderFacts = []
    
    def addFact(self, ordFact):
        ordFact.setId(self.ids)
        self.ids += 1
        self.orderFacts.append(ordFact)
    
    def onReceive(self, stat, msg):
        '''
        收回報callback: 參考永豐API格式
        '''
        logging.INFO(f"Receive {stat} Report")
        if "trade_id" in msg:
            # 成交
            ordId = msg["trade_id"]
            rpt = FuturesOrdDealRpt(**msg)
        else:
            # 委託
            ordId = msg["order"]["id"]
            rpt = FuturesOrdRpt(**msg)
        factId = self.ordMgr.getOrd(ordId).factId
        self.orderFacts[factId].onReceive(rpt)
        

        