from .errors import InvalidQuantity, ReasonRequired, NegativeStockNotAllowed, InvalidSKU, InvalidProductName, InvalidProductIdentity

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

def is_valid_sku(sku: str) -> bool:
    if not sku or not str(sku).strip():
        return False
    s = str(sku).strip()
    if s.isdigit():
        return False
    if len(s) < 3:
        return False
    if " " in s:
        return False
    return True

def is_valid_name(name: str) -> bool:
    if not name or not str(name).strip():
        return False
    n = str(name).strip()
    if len(n) < 3:
        return False
    return True

def is_valid_product_for_kiosk(sku: str, name: str) -> bool:
    return is_valid_sku(sku) and is_valid_name(name)

def validate_sku(sku: str):
    if not is_valid_sku(sku):
        raise InvalidSKU()

def validate_name(name: str):
    if not is_valid_name(name):
        raise InvalidProductName()

def validate_product_identity(sku: str, name: str):
    if not is_valid_product_for_kiosk(sku, name):
        raise InvalidProductIdentity()
