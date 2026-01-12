from django.core.management.base import BaseCommand
from contact.modules.reorder.application.commands.run_reorder_engine_cmd import execute


class Command(BaseCommand):
    help = "Run reorder engine v1"

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true")
        parser.add_argument("--apply", action="store_true")
        parser.add_argument("--limit", type=int, default=100)

    def handle(self, *args, **options):
        dry = options.get("dry_run", False)
        app = options.get("apply", False)
        limit = int(options.get("limit", 100))
        cnt = execute(dry_run=dry, apply=app, limit=limit)
        self.stdout.write(self.style.SUCCESS(f"processed: {cnt} (limit={limit})"))
