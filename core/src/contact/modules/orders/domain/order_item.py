from dataclasses import dataclass


@dataclass
class OrderItem:
    order_id: int
    product_ref: str
    qty: int

