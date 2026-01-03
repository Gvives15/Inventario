class InventoryError(Exception):
    pass

class InvalidQuantity(InventoryError):
    def __init__(self, message="quantity must be positive"):
        super().__init__(message)

class ReasonRequired(InventoryError):
    def __init__(self, message="reason is required for adjustments"):
        super().__init__(message)

class NegativeStockNotAllowed(InventoryError):
    def __init__(self, message="stock cannot go negative"):
        super().__init__(message)

class ProductListNotFound(InventoryError):
    def __init__(self, message="product list not found"):
        super().__init__(message)

class ProductListInactive(InventoryError):
    def __init__(self, message="product list inactive"):
        super().__init__(message)

class ProductListEmpty(InventoryError):
    def __init__(self, message="product list has no items"):
        super().__init__(message)

class InvalidSKU(InventoryError):
    def __init__(self, message="invalid sku"):
        super().__init__(message)

class InvalidProductName(InventoryError):
    def __init__(self, message="invalid product name"):
        super().__init__(message)

class InvalidProductIdentity(InventoryError):
    def __init__(self, message="invalid product identity"):
        super().__init__(message)
