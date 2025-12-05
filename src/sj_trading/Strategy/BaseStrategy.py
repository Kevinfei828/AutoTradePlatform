import shioaji as sj
from abc import ABC, abstractmethod
from shioaji import TickFOPv1, Exchange
from sj_trading.Order.Order import OrderFactBase
from sj_trading.Utils.Constant import *
from sj_trading.Utils.Order import Position

class BaseStrategy:
    def __init__(self, **kwargs):
        self.orderFacts: list[OrderFactBase] = []
        self.currOrderFact: OrderFactBase = None
        self.quote_sub_id = -1
        self.symbol = kwargs.get('symbol', None)
        self.use_ha = kwargs.get('use_ha', True)
        self.exit = kwargs.get('exit', None)
        self.exit_tick = kwargs.get('exit_tick', 0)
        
        # 下單變數
        self.pos = Position()
        
    def _set_ord_act(self):
        if self.pos.type == PositionType.LONG:
            action = sj.constant.Action.Sell
        elif self.pos.type == PositionType.SHORT:
            action = sj.constant.Action.Buy
        return action
        
    def _setPosition(self, **new_pos):
        for k, v in new_pos:
            setattr(self.pos, k, v)
    
    def _check_exit(
        self,
        close,
        atr=None
    ):
        if self.pos.size == 0:
            return

        if self.exit == EXIT_DEFAULT:
            self.currOrderFact.onOrder(self._set_ord_act(), close)
    
        elif (self.exit == EXIT_TICK and abs(close - self.pos.price) >= self.exit_tick) or \
            (self.exit == EXIT_ATR and atr is not None and abs(close - atr) >= self.exit_tick):
            self.currOrderFact.onOrder(self._set_ord_act(), close)

        self._setPosition(
            price=None,
            type=PositionType.EMPTY,
            size=0,
        )
    
    # TODO: 目前只允許一種order，未來隨下單size>1開放成list[order]
    # def addOrderFact(self, orderFact):
    #     self.orderFacts.append(orderFact)
        
    def setCurrOrderFact(self, orderFact):
        self.currOrderFact = orderFact
        # if orderFact not in self.orderFacts:
        #     self.addOrderFact(orderFact)
    
    @abstractmethod
    def OnTick(self, tick, **kwargs) -> int:
        pass