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
