from django.core.management.base import BaseCommand
from inventory.infrastructure.orm.product_repo import create as create_product
from inventory.infrastructure.orm.models import Product

class Command(BaseCommand):
    help = "Cargar productos demo (por defecto 10)"

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=10)
        parser.add_argument("--prefix", type=str, default="DEMO")
        parser.add_argument("--category", type=str, default="General")

    def handle(self, *args, **options):
        count = options["count"]
        prefix = options["prefix"]
        category = options["category"]

        created = 0
        for i in range(1, count + 1):
            sku = f"{prefix}-{i:03d}"
            if Product.objects.filter(sku=sku).exists():
                continue
            name = f"Producto {i}"
            create_product(name=name, sku=sku, category=category, stock_minimum=0)
            created += 1
        self.stdout.write(self.style.SUCCESS(f"Productos creados: {created}/{count}"))
