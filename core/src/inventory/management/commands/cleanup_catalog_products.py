from django.core.management.base import BaseCommand
from django.db import transaction
from inventory.infrastructure.orm.models import Product, StockMovement, ProductListItemModel
from inventory.domain.rules import is_valid_product_for_kiosk

class Command(BaseCommand):
    help = "Audita y limpia el catálogo: desactiva inválidos y los remueve de listas; borra solo si no está referenciado"

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true")
        parser.add_argument("--apply", action="store_true")
        parser.add_argument("--delete-unreferenced", action="store_true")
        parser.add_argument("--deactivate-invalid", action="store_true")

    def handle(self, *args, **options):
        dry = options["dry_run"]
        apply = options["apply"]
        delete_unref = options["delete_unreferenced"]
        deactivate = options["deactivate_invalid"]

        products = list(Product.objects.all())
        invalid = [p for p in products if not is_valid_product_for_kiosk(p.sku, p.name)]
        total = len(products)
        in_lists = ProductListItemModel.objects.filter(product__in=invalid).count()
        refs_stock = StockMovement.objects.filter(product__in=invalid).count()
        can_delete = []
        cannot_delete = []
        for p in invalid:
            has_list = ProductListItemModel.objects.filter(product=p).exists()
            has_stock = StockMovement.objects.filter(product=p).exists()
            if not has_list and not has_stock:
                can_delete.append(p)
            else:
                cannot_delete.append(p)

        self.stdout.write(self.style.WARNING(f"total products: {total}"))
        self.stdout.write(self.style.WARNING(f"invalid found: {len(invalid)}"))
        self.stdout.write(self.style.WARNING(f"invalid in lists: {in_lists}"))
        self.stdout.write(self.style.WARNING(f"invalid referenced in stock: {refs_stock}"))
        self.stdout.write(self.style.WARNING(f"deletable: {len(can_delete)} non_deletable: {len(cannot_delete)}"))

        if not apply:
            return

        with transaction.atomic():
            for p in invalid:
                ProductListItemModel.objects.filter(product=p).delete()
            if deactivate:
                for p in invalid:
                    if p.is_active:
                        p.is_active = False
                        p.save(update_fields=["is_active", "updated_at"])
            if delete_unref:
                for p in can_delete:
                    p.delete()
        self.stdout.write(self.style.SUCCESS("cleanup applied"))
