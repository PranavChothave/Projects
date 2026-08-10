class OrderException(Exception):
    pass

class InvalidCountryException(OrderException):
    pass

class AmountLimitException(OrderException):
    pass

class DuplicateOrderException(OrderException):
    pass

class InvalidOrderDataException(OrderException):
    pass
