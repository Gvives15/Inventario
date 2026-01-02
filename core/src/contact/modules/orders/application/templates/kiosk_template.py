import re
from contact.shared.domain.errors import InvalidTemplateItem

TEMPLATE = [
    {"product_ref": "SKU:COCA-2250ML", "qty": 12},
    {"product_ref": "SKU:AGUA-2000ML", "qty": 6},
    {"product_ref": "SKU:YERBA-1000G", "qty": 6},
    {"product_ref": "SKU:AZUCAR-1000G", "qty": 6},
    {"product_ref": "SKU:ARROZ-1000G", "qty": 6},
    {"product_ref": "SKU:FIDEOS-500G", "qty": 12},
    {"product_ref": "SKU:ACEITE-900ML", "qty": 6},
    {"product_ref": "SKU:SAL-500G", "qty": 12},
    {"product_ref": "SKU:GALLETA-300G", "qty": 12},
    {"product_ref": "SKU:LECHE-1000ML", "qty": 12},
    {"product_ref": "SKU:TE-50U", "qty": 6},
    {"product_ref": "SKU:CAFE-500G", "qty": 6},
]

# El formato es SKU: seguido de uno o más grupos de letras mayúsculas y números,
# separados por guiones opcionales.
SKU_RE = re.compile(r"^SKU:[A-Z0-9]+(?:-[A-Z0-9]+)*$")


def _validate(items: list[dict]) -> list[dict]:
    if not (10 <= len(items) <= 15):
        raise InvalidTemplateItem("", 0, "template size must be between 10 and 15")
    for it in items:
        ref = str(it.get("product_ref", ""))
        qty = int(it.get("qty", 0))
        if not ref or not SKU_RE.match(ref):
            raise InvalidTemplateItem(ref, qty, "invalid product_ref format")
        if qty <= 0:
            raise InvalidTemplateItem(ref, qty, "invalid qty")
    return items


def get_kiosk_template() -> list[dict]:
    return _validate(TEMPLATE.copy())
