from .errors import InvalidQuantity, ReasonRequired, NegativeStockNotAllowed

def validate_positive(quantity: int):
    if quantity <= 0:
        raise InvalidQuantity()

def require_reason(reason: str):
    if not reason or not reason.strip():
        raise ReasonRequired()

def ensure_non_negative(new_stock: int):
    if new_stock < 0:
        raise NegativeStockNotAllowed()

def normalize_sku(raw: str) -> str:
    sku = (raw or "").strip().upper()
    if not sku:
        raise ValueError("sku is required")
    return sku
