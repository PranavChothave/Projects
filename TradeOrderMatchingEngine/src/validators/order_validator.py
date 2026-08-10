from src.exceptions.order_exceptions import *
from src.models.order import TradeType

APPROVED_COUNTRIES = {"US", "UK", "IN", "SG", "JP", "DE", "FR"}

MAX_LIMITS = {
    TradeType.EQUITY: 100_000,
    TradeType.FOREX: 500_000,
    TradeType.CRYPTO: 50_000
}

class OrderValidator:

    @staticmethod
    def validate(order):
        if order.country not in APPROVED_COUNTRIES:
            raise InvalidCountryException(order.country)

        if order.price <= 0 or order.quantity <= 0:
            raise InvalidOrderDataException("Price/Quantity must be positive")

        max_value = MAX_LIMITS[order.trade_type]
        if order.price * order.quantity > max_value:
            raise AmountLimitException(order.trade_type, max_value)
