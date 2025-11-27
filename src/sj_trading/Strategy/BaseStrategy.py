from abc import ABC, abstractmethod
from shioaji import TickFOPv1, Exchange

class BaseStrategy:
    def __init__(self):
        self.orderFacts = []
    
    def addOrderFact(self, orderFact):
        self.orderFacts.append(orderFact)
    
    @abstractmethod
    def OnTick(self, tick: TickFOPv1) -> int:
        pass
    
    @abstractmethod
    def OnAfterTick(self, res):
        pass