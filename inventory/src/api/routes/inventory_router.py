from ninja import Router
from ninja.errors import HttpError
from django.shortcuts import get_object_or_404
from inventory.src.api.schemas.product_schemas import ProductCreateIn, ProductOut, ProductPatchIn, MovementOut
from inventory.src.api.schemas.stock_schemas import StockEntryIn, StockExitIn, AdjustToCountIn, AdjustDeltaIn
from inventory.src.infrastructure.orm.product_repo import create as create_product, update_partial, list_products
from inventory.src.infrastructure.orm.models import Product
from inventory.src.application.commands.record_entry_cmd import execute as record_entry
from inventory.src.application.commands.record_exit_cmd import execute as record_exit
from inventory.src.application.commands.adjust_to_count_cmd import execute as adjust_to_count
from inventory.src.application.commands.adjust_delta_cmd import execute as adjust_delta
from inventory.src.application.queries.list_movements_q import execute as list_movements
from inventory.src.application.queries.list_low_stock_q import execute as list_low_stock

router = Router()

@router.post("/products", response=ProductOut)
def create_product_ep(request, payload: ProductCreateIn):
    p = create_product(payload.name, payload.sku, payload.category or "", payload.stock_minimum or 0)
    return ProductOut(
        id=p.id,
        name=p.name,
        sku=p.sku,
        category=p.category,
        stock_current=p.stock_current,
        stock_minimum=p.stock_minimum,
        is_active=p.is_active,
    )

@router.get("/products", response=list[ProductOut])
def list_products_ep(request, search: str | None = None, category: str | None = None):
    qs = list_products(search, category)
    return [
        ProductOut(
            id=p.id,
            name=p.name,
            sku=p.sku,
            category=p.category,
            stock_current=p.stock_current,
            stock_minimum=p.stock_minimum,
            is_active=p.is_active,
        )
        for p in qs
    ]

@router.get("/products/{id}", response=ProductOut)
def get_product_ep(request, id: int):
    p = get_object_or_404(Product, id=id)
    return ProductOut(
        id=p.id,
        name=p.name,
        sku=p.sku,
        category=p.category,
        stock_current=p.stock_current,
        stock_minimum=p.stock_minimum,
        is_active=p.is_active,
    )

@router.patch("/products/{id}", response=ProductOut)
def patch_product_ep(request, id: int, payload: ProductPatchIn):
    # stock_current no está en el schema; extra=forbid previene su uso
    p = get_object_or_404(Product, id=id)
    fields = {}
    if payload.name is not None:
        fields["name"] = payload.name
    if payload.category is not None:
        fields["category"] = payload.category
    if payload.stock_minimum is not None:
        fields["stock_minimum"] = payload.stock_minimum
    p = update_partial(p, **fields) if fields else p
    return ProductOut(
        id=p.id,
        name=p.name,
        sku=p.sku,
        category=p.category,
        stock_current=p.stock_current,
        stock_minimum=p.stock_minimum,
        is_active=p.is_active,
    )

@router.post("/stock/entry", response=ProductOut)
def stock_entry_ep(request, payload: StockEntryIn):
    p = record_entry(payload.product_id, payload.quantity, payload.reason or "", getattr(request, "user", None))
    return ProductOut(
        id=p.id,
        name=p.name,
        sku=p.sku,
        category=p.category,
        stock_current=p.stock_current,
        stock_minimum=p.stock_minimum,
        is_active=p.is_active,
    )

@router.post("/stock/exit", response=ProductOut)
def stock_exit_ep(request, payload: StockExitIn):
    p = record_exit(payload.product_id, payload.quantity, payload.reason or "", getattr(request, "user", None))
    return ProductOut(
        id=p.id,
        name=p.name,
        sku=p.sku,
        category=p.category,
        stock_current=p.stock_current,
        stock_minimum=p.stock_minimum,
        is_active=p.is_active,
    )

@router.post("/stock/adjust-to-count", response=ProductOut)
def stock_adjust_to_count_ep(request, payload: AdjustToCountIn):
    p = adjust_to_count(payload.product_id, payload.counted_stock, payload.reason or "", getattr(request, "user", None))
    return ProductOut(
        id=p.id,
        name=p.name,
        sku=p.sku,
        category=p.category,
        stock_current=p.stock_current,
        stock_minimum=p.stock_minimum,
        is_active=p.is_active,
    )

@router.post("/stock/adjust-delta", response=ProductOut)
def stock_adjust_delta_ep(request, payload: AdjustDeltaIn):
    p = adjust_delta(payload.product_id, payload.delta, payload.reason or "", getattr(request, "user", None))
    return ProductOut(
        id=p.id,
        name=p.name,
        sku=p.sku,
        category=p.category,
        stock_current=p.stock_current,
        stock_minimum=p.stock_minimum,
        is_active=p.is_active,
    )

@router.get("/products/{id}/movements", response=list[MovementOut])
def list_movements_ep(request, id: int, limit: int = 50):
    items = list_movements(id, limit)
    return [
        MovementOut(
            id=m.id,
            delta=m.delta,
            movement_type=m.movement_type,
            reason=m.reason,
            resulting_stock=m.resulting_stock,
            created_at=m.created_at.isoformat(),
        )
        for m in items
    ]

@router.get("/alerts/low-stock", response=list[ProductOut])
def list_low_stock_ep(request):
    qs = list_low_stock()
    return [
        ProductOut(
            id=p.id,
            name=p.name,
            sku=p.sku,
            category=p.category,
            stock_current=p.stock_current,
            stock_minimum=p.stock_minimum,
            is_active=p.is_active,
        )
        for p in qs
    ]
