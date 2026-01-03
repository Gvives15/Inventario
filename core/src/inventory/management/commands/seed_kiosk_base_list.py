from django.core.management.base import BaseCommand, CommandError
from inventory.infrastructure.orm.models import Product, ProductListModel, ProductListItemModel
from inventory.domain.rules import is_valid_product_for_kiosk

class Command(BaseCommand):
    help = "Seed kiosk_base product list"

    def add_arguments(self, parser):
        parser.add_argument("--code", type=str, default="kiosk_base")
        parser.add_argument("--limit", type=int, default=15)

    def handle(self, *args, **options):
        code = options["code"]
        limit = options["limit"]
        products_qs = Product.objects.filter(is_active=True).order_by("-created_at", "-id")
        count = products_qs.count()
        if count == 0:
            self.stdout.write(self.style.WARNING("no hay productos"))
            return
        plist, _ = ProductListModel.objects.get_or_create(code=code, defaults={"name": code, "is_active": True})
        existing = set(ProductListItemModel.objects.filter(product_list=plist).values_list("product_id", flat=True))
        valid_products = [p for p in products_qs if is_valid_product_for_kiosk(p.sku, p.name)]
        if len(valid_products) < 10:
            raise CommandError(f"insufficient valid products: {len(valid_products)} found")
        to_create = []
        sort = 0
        for p in valid_products[:limit]:
            if p.id in existing:
                continue
            sort += 1
            to_create.append(ProductListItemModel(product_list=plist, product=p, default_qty=2, sort_order=sort))
        if to_create:
            ProductListItemModel.objects.bulk_create(to_create)
        total_items = ProductListItemModel.objects.filter(product_list=plist).count()
        items_qs = ProductListItemModel.objects.filter(product_list=plist).select_related("product")
        invalid_detected = any(not is_valid_product_for_kiosk(i.product.sku, i.product.name) for i in items_qs)
        if invalid_detected:
            raise CommandError("invalid product detected in kiosk_base after seed")
        self.stdout.write(self.style.SUCCESS(f"lista {code} lista con {total_items} items"))
