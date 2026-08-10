import os
import csv
from src.engine.matching_engine import MatchingEngine
from src.validators.order_validator import OrderValidator
from src.utils.csv_loader import load_orders
from src.models.order import OrderStatus

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

engine = MatchingEngine()

orders = (
    load_orders("data/buy_orders.csv") +
    load_orders("data/sell_orders.csv")
)

print(f"Loaded BUY orders : {len([o for o in orders if o.order_type.value == 'BUY'])}")
print(f"Loaded SELL orders: {len([o for o in orders if o.order_type.value == 'SELL'])}")



for order in orders:
    try:
        OrderValidator.validate(order)
        engine.submit_order(order)
    except Exception:
        order.status = OrderStatus.REJECTED
        engine.all_orders.append(order)

summary = engine.generate_summary()

print("\n================ TRADE SUMMARY ================\n")
print(f"Total Orders Processed : {summary['total_orders']}")
print(f"Buy Orders             : {summary['buy_orders']}")
print(f"Sell Orders            : {summary['sell_orders']}")
print(f"Successful Trades      : {summary['total_trades']}")
print(f"Rejected Orders        : {summary['rejected_orders']}")
print(f"Fully Filled Orders    : {summary['filled_orders']}")
print(f"Partially Filled       : {summary['partially_filled_orders']}")
print(f"Open Orders Remaining  : {summary['open_orders']}")

print("\n--- Trade Type Breakdown ---")
for k, v in summary.items():
    if k.endswith("_trades"):
        print(f"{k.replace('_', ' ').upper()} : {v}")

print("\n===============================================\n")


with open(f"{OUTPUT_DIR}/trade_summary.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["buy_order", "sell_order", "trade_type", "price", "quantity", "timestamp"])
    for t in engine.trades:
        writer.writerow([
            t.buy_order_id,
            t.sell_order_id,
            t.trade_type,
            t.price,
            t.quantity,
            t.timestamp
        ])
