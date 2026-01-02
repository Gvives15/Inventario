class ContactNotFound(Exception):
    pass


class MissingMinData(Exception):
    pass


class InvalidTemplateItem(Exception):
    def __init__(self, product_ref: str, qty: int, reason: str):
        super().__init__(f"invalid item: ref={product_ref} qty={qty} reason={reason}")
        self.product_ref = product_ref
        self.qty = qty
        self.reason = reason

