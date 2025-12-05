from pydantic import BaseModel, Field
from typing import Optional

class OrderOperation(BaseModel):
    op_type: str
    op_code: str
    op_msg: str

    class Config:
        extra = "ignore"

class OrderAccount(BaseModel):
    account_type: str
    person_id: str
    broker_id: str
    account_id: str
    signed: bool

    class Config:
        extra = "ignore"

class FuturesOrderDetail(BaseModel):
    id: str
    seqno: str
    ordno: str
    account: OrderAccount

    action: str        
    price: float
    quantity: int

    order_type: str      
    price_type: str     
    market_type: str     
    oc_type: str         
    subaccount: str
    combo: bool

    class Config:
        extra = "ignore"


class OrderStatus(BaseModel):
    id: str
    exchange_ts: float
    modified_price: float
    cancel_quantity: int
    order_quantity: int
    web_id: str

    class Config:
        extra = "ignore"

class FuturesContract(BaseModel):
    security_type: str   
    code: str             
    exchange: str       
    delivery_month: str
    delivery_date: str
    strike_price: float
    option_right: str

    class Config:
        extra = "ignore"

class FuturesOrdRpt(BaseModel):
    '''
    期貨委託回報
    '''
    operation: OrderOperation
    order: FuturesOrderDetail
    status: OrderStatus
    contract: FuturesContract

    class Config:
        extra = "ignore"