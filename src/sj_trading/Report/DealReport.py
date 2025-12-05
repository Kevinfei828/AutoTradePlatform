from pydantic import BaseModel

class FuturesOrdDealRpt(BaseModel):
    trade_id: str
    seqno: str
    ordno: str
    exchange_seq: str
    broker_id: str
    account_id: str
    action: str
    code: str
    price: float
    quantity: int
    subaccount: str
    security_type: str
    delivery_month: str
    strike_price: float
    option_right: str
    market_type: str
    combo: bool
    ts: float