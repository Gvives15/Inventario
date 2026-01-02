from ninja import Schema
from typing import Optional

class ProductCreateIn(Schema):
    name: str
    sku: str
    category: Optional[str] = None
    stock_minimum: Optional[int] = 0

class ProductPatchIn(Schema):
    name: Optional[str] = None
    category: Optional[str] = None
    stock_minimum: Optional[int] = None
    
    class Config:
        extra = "forbid"

class ProductOut(Schema):
    id: int
    name: str
    sku: str
    category: Optional[str] = None
    stock_current: int
    stock_minimum: int
    is_active: bool

class MovementOut(Schema):
    id: int
    delta: int
    movement_type: str
    reason: Optional[str] = None
    resulting_stock: int
    created_at: str
