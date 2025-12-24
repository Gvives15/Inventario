from django.db.models import Q, F
from django.db import transaction
from inventory.src.infrastructure.orm.models import Product
from inventory.src.domain.rules import normalize_sku

def get_for_update(product_id: int) -> Product:
    return Product.objects.select_for_update().get(id=product_id)

def create(name: str, sku: str, category: str, stock_minimum: int) -> Product:
    s = normalize_sku(sku)
    return Product.objects.create(name=name, sku=s, category=category, stock_minimum=stock_minimum)

def update_partial(product: Product, **fields) -> Product:
    if "sku" in fields and fields["sku"] is not None:
        fields["sku"] = normalize_sku(fields["sku"])
    for k, v in fields.items():
        setattr(product, k, v)
    product.save(update_fields=list(fields.keys()))
    return product

def list_products(search: str | None = None, category: str | None = None):
    qs = Product.objects.all()
    if search:
        qs = qs.filter(Q(name__icontains=search) | Q(sku__icontains=search))
    if category:
        qs = qs.filter(category__iexact=category)
    return qs.order_by("name", "sku")

def list_low_stock():
    return Product.objects.filter(is_active=True).filter(stock_current__lte=F("stock_minimum"))
