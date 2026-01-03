import json
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.test import Client
from contact.models import Contact, ConversationStateModel, OrderModel, OrderItemModel, MessageInboundModel
from inventory.infrastructure.orm.models import ProductListModel, ProductListItemModel
from inventory.domain.rules import is_valid_product_for_kiosk

class Command(BaseCommand):
    help = "E2E demo: WhatsApp inbound E1 -> E2 PROPOSED with dedupe and idempotency"

    def add_arguments(self, parser):
        parser.add_argument("--whatsapp-id", type=str, default="5491199999999")
        parser.add_argument("--code", type=str, default="kiosk_base")
        parser.add_argument("--limit", type=int, default=15)
        parser.add_argument("--reset", action="store_true")

    def handle(self, *args, **options):
        wh = options["whatsapp_id"]
        code = options["code"]
        limit = options["limit"]
        reset = options["reset"]

        if reset:
            c = Contact.objects.filter(whatsapp_id=wh).first()
            if c:
                MessageInboundModel.objects.filter(whatsapp_id=wh).delete()
                OrderModel.objects.filter(contact=c).delete()
                ConversationStateModel.objects.filter(contact=c).delete()
                c.name = ""
                c.zone = ""
                c.business_type = ""
                c.save(update_fields=["name", "zone", "business_type", "updated_at"])
            self.stdout.write(self.style.WARNING(f"reset aplicado para {wh}"))

        call_command("seed_kiosk_base_list", code=code, limit=limit)
        try:
            plist = ProductListModel.objects.get(code=code)
            items = list(ProductListItemModel.objects.filter(product_list=plist).select_related("product")[:5])
            invalid_in_list = [i for i in items if not is_valid_product_for_kiosk(i.product.sku, i.product.name)]
            print(f"kiosk_base items count: {ProductListItemModel.objects.filter(product_list=plist).count()}")
            for i in items:
                print(f"item: {i.product.sku} - {i.product.name}")
            if invalid_in_list:
                raise SystemExit(1)
        except ProductListModel.DoesNotExist:
            raise SystemExit(1)

        client = Client()
        url = "/api/contacts/webhooks/whatsapp/inbound"

        # 1) Mensaje libre (nuevo contacto) -> pide E1
        payload1 = {
            "provider": "whatsapp_mock",
            "provider_message_id": f"e2e_{wh}_001",
            "whatsapp_id": wh,
            "text": "Hola, quiero pedir",
            "raw_payload": {},
        }
        r1 = client.post(url, data=json.dumps(payload1), content_type="application/json")
        self.stdout.write(self.style.SUCCESS(f"Paso 1 reply: {getattr(r1, 'json', lambda: {})().get('reply')}"))
        self._print_db_step1(wh)

        # 2) Dedupe (mismo provider_message_id)
        r2 = client.post(url, data=json.dumps(payload1), content_type="application/json")
        self.stdout.write(self.style.SUCCESS(f"Paso 2 reply: {getattr(r2, 'json', lambda: {})().get('reply')}"))
        self._print_inbound_count(wh)

        # 3) E1 parcial (Nombre)
        payload3 = {
            "provider": "whatsapp_mock",
            "provider_message_id": f"e2e_{wh}_002",
            "whatsapp_id": wh,
            "text": "Nombre: Pedro",
            "raw_payload": {},
        }
        r3 = client.post(url, data=json.dumps(payload3), content_type="application/json")
        self.stdout.write(self.style.SUCCESS(f"Paso 3 reply: {getattr(r3, 'json', lambda: {})().get('reply')}"))
        self._print_contact_min(wh)

        # 4) E1 completo (Zona + Tipo) -> dispara E2
        payload4 = {
            "provider": "whatsapp_mock",
            "provider_message_id": f"e2e_{wh}_003",
            "whatsapp_id": wh,
            "text": "Zona: Norte\nTipo: Kiosco",
            "raw_payload": {},
        }
        r4 = client.post(url, data=json.dumps(payload4), content_type="application/json")
        self.stdout.write(self.style.SUCCESS(f"Paso 4 reply: {getattr(r4, 'json', lambda: {})().get('reply')}"))
        self._print_invariants_step4(wh)

        # 5) Idempotencia: reenvía misma propuesta
        payload5 = {
            "provider": "whatsapp_mock",
            "provider_message_id": f"e2e_{wh}_004",
            "whatsapp_id": wh,
            "text": "Gracias master",
            "raw_payload": {},
        }
        r5 = client.post(url, data=json.dumps(payload5), content_type="application/json")
        self.stdout.write(self.style.SUCCESS(f"Paso 5 reply: {getattr(r5, 'json', lambda: {})().get('reply')}"))
        self._print_orders_count(wh)

    def _print_db_step1(self, wh: str):
        inbound_cnt = MessageInboundModel.objects.filter(whatsapp_id=wh).count()
        c = Contact.objects.filter(whatsapp_id=wh).first()
        st = ConversationStateModel.objects.filter(contact=c).first() if c else None
        orders_cnt = OrderModel.objects.filter(contact=c).count() if c else 0
        print(f"inbound: {inbound_cnt}")
        print(f"contact: {bool(c)}")
        print(f"stage: {getattr(st, 'stage', None)}")
        print(f"orders: {orders_cnt}")

    def _print_inbound_count(self, wh: str):
        inbound_cnt = MessageInboundModel.objects.filter(whatsapp_id=wh).count()
        print(f"inbound: {inbound_cnt}")

    def _print_contact_min(self, wh: str):
        c = Contact.objects.get(whatsapp_id=wh)
        st = ConversationStateModel.objects.get(contact=c)
        print(f"name: {c.name} zone: {c.zone} type: {c.business_type}")
        print(f"stage: {st.stage}")

    def _print_invariants_step4(self, wh: str):
        c = Contact.objects.get(whatsapp_id=wh)
        st = ConversationStateModel.objects.get(contact=c)
        o = OrderModel.objects.get(id=st.last_order_id)
        items_cnt = OrderItemModel.objects.filter(order=o).count()
        print(f"stage: {st.stage} last_order_id: {st.last_order_id}")
        print(f"order_status: {o.status}")
        print(f"items: {items_cnt}")

    def _print_orders_count(self, wh: str):
        c = Contact.objects.get(whatsapp_id=wh)
        st = ConversationStateModel.objects.get(contact=c)
        cnt = OrderModel.objects.filter(contact=c).count()
        print(f"orders_count: {cnt} last_order_id: {st.last_order_id}")
