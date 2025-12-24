from ninja import Schema

class StockEntryIn(Schema):
    product_id: int
    quantity: int
    reason: str | None = ""

class StockExitIn(Schema):
    product_id: int
    quantity: int
    reason: str | None = ""

class AdjustToCountIn(Schema):
    product_id: int
    counted_stock: int
    reason: str | None = ""

class AdjustDeltaIn(Schema):
    product_id: int
    delta: int
    reason: str | None = ""
