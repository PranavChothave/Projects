from src.engine.order_book import OrderBook
from src.models.trade import Trade
from src.models.order import OrderStatus
from datetime import datetime
from collections import defaultdict

class MatchingEngine:

    def __init__(self):
        self.order_books = {}
        self.trades = []
        self.all_orders = []

    def get_book(self, trade_type):
        if trade_type not in self.order_books:
            self.order_books[trade_type] = OrderBook()
        return self.order_books[trade_type]

    def submit_order(self, order):
        self.all_orders.append(order)
        book = self.get_book(order.trade_type)
        book.add_order(order)
        self.match(book)

    def match(self, book):
        with book.lock:
            while book.buy_orders and book.sell_orders:
                buy_price, _, buy = book.buy_orders[0]
                sell_price, _, sell = book.sell_orders[0]

                if -buy_price < sell_price:
                    break

                qty = min(buy.remaining_qty, sell.remaining_qty)
                trade_price = sell.price

                buy.remaining_qty -= qty
                sell.remaining_qty -= qty

                self.trades.append(
                    Trade(
                        buy.order_id,
                        sell.order_id,
                        buy.trade_type.value,
                        trade_price,
                        qty,
                        datetime.now()
                    )
                )

                if buy.remaining_qty == 0:
                    buy.status = OrderStatus.FILLED
                    book.buy_orders.pop(0)
                else:
                    buy.status = OrderStatus.PARTIALLY_FILLED

                if sell.remaining_qty == 0:
                    sell.status = OrderStatus.FILLED
                    book.sell_orders.pop(0)
                else:
                    sell.status = OrderStatus.PARTIALLY_FILLED

    def generate_summary(self):
        summary = defaultdict(int)

        for o in self.all_orders:
            summary["total_orders"] += 1
            summary[f"{o.order_type.value.lower()}_orders"] += 1

            if o.status == OrderStatus.REJECTED:
                summary["rejected_orders"] += 1
            elif o.status == OrderStatus.FILLED:
                summary["filled_orders"] += 1
            elif o.status == OrderStatus.PARTIALLY_FILLED:
                summary["partially_filled_orders"] += 1
            else:
                summary["open_orders"] += 1

        summary["total_trades"] = len(self.trades)

        for t in self.trades:
            summary[f"{t.trade_type.lower()}_trades"] += 1

        return summary
