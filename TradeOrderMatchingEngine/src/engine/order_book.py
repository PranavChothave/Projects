import threading
import heapq

class OrderBook:
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []
        self.lock = threading.Lock()

    def add_order(self, order):
        with self.lock:
            if order.order_type.name == "BUY":
                heapq.heappush(self.buy_orders, (-order.price, order.timestamp, order))
            else:
                heapq.heappush(self.sell_orders, (order.price, order.timestamp, order))
