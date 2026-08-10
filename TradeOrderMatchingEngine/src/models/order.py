from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

class TradeType(Enum):
    EQUITY = "EQUITY"
    FOREX = "FOREX"
    CRYPTO = "CRYPTO"

class OrderType(Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderStatus(Enum):
    PENDING = "PENDING"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    REJECTED = "REJECTED"

@dataclass(order=True)
class Order:
    sort_index: tuple = field(init=False, repr=False)
    order_id: str
    trader_id: str
    trade_type: TradeType
    order_type: OrderType
    price: float
    quantity: int
    country: str
    timestamp: datetime
    remaining_qty: int = field(init=False)
    status: OrderStatus = OrderStatus.PENDING

    def __post_init__(self):
        self.remaining_qty = self.quantity
        self.sort_index = (self.price, self.timestamp)
