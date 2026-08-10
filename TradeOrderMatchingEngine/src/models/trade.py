from dataclasses import dataclass
from datetime import datetime

@dataclass
class Trade:
    buy_order_id: str
    sell_order_id: str
    trade_type: str
    price: float
    quantity: int
    timestamp: datetime
