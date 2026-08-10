import csv
from datetime import datetime
from pathlib import Path
from src.models.order import Order, TradeType, OrderType

BASE_DIR = Path(__file__).resolve().parents[2]  # project root


def load_orders(relative_path):
    orders = []
    file_path = BASE_DIR / relative_path

    print(f"[DEBUG] Looking for file at: {file_path}")

    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            try:
                orders.append(
                    Order(
                        order_id=row["orderId"],
                        trader_id=row["traderId"],
                        trade_type=TradeType[row["tradeType"]],
                        order_type=OrderType[row["orderType"]],
                        price=float(row["price"]),
                        quantity=int(row["quantity"]),
                        country=row["countryCode"],
                        timestamp=datetime.strptime(
                            row["timestamp"], "%Y-%m-%d %H:%M:%S"
                        )
                    )
                )
            except Exception as e:
                print(f"[WARN] Skipping invalid row: {row}")
                print(f"[WARN] Reason: {e}")

    return orders
