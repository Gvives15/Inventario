from ninja import Schema
from pydantic import BaseModel
from pydantic.config import ConfigDict

class ProductCreateIn(Schema):
    name: str
    sku: str
    category: str | None = ""
    stock_minimum: int = 0

class ProductPatchIn(Schema):
    model_config = ConfigDict(extra='forbid')
    name: str | None = None
    category: str | None = None
    stock_minimum: int | None = None

class ProductOut(Schema):
    id: int
    name: str
    sku: str
    category: str
    stock_current: int
    stock_minimum: int
    is_active: bool

class MovementOut(Schema):
    id: int
    delta: int
    movement_type: str
    reason: str
    resulting_stock: int
    created_at: str
