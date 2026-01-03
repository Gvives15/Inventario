from inventory.infrastructure.orm.models import Product

def execute(skus: list[str]) -> dict[str, str]:
    if not skus:
        return {}
    qs = Product.objects.filter(sku__in=skus).values("sku", "name")
    out = {x["sku"]: x["name"] for x in qs}
    return out
