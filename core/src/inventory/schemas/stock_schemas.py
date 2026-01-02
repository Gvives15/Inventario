from ninja import Schema
from typing import Optional

class StockEntryIn(Schema):
    product_id: int
    quantity: int
    reason: Optional[str] = None

class StockExitIn(Schema):
    product_id: int
    quantity: int
    reason: Optional[str] = None

class AdjustToCountIn(Schema):
    product_id: int
    counted_stock: int
    reason: Optional[str] = None

class AdjustDeltaIn(Schema):
    product_id: int
    delta: int
    reason: Optional[str] = None
