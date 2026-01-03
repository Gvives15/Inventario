import json
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.test import Client

class Command(BaseCommand):
    help = "E2E demo T3: editar y confirmar pedido. Comandos: + SKU qty (agregar), - SKU (quitar), = SKU qty (setear)"

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

        client = Client()
        url = "/api/contacts/webhooks/whatsapp/inbound"
        if reset:
            call_command("demo_e2e_task2", "--reset", "--whatsapp-id", wh, "--code", code, "--limit", limit)
        else:
            call_command("seed_kiosk_base_list", code=code, limit=limit)
            client.post(url, data=json.dumps({"provider":"whatsapp_mock","provider_message_id":f"t3_{wh}_1","whatsapp_id":wh,"text":"Hola","raw_payload":{}}), content_type="application/json")
            client.post(url, data=json.dumps({"provider":"whatsapp_mock","provider_message_id":f"t3_{wh}_2","whatsapp_id":wh,"text":"Nombre: Juan","raw_payload":{}}), content_type="application/json")
            client.post(url, data=json.dumps({"provider":"whatsapp_mock","provider_message_id":f"t3_{wh}_3","whatsapp_id":wh,"text":"Zona: Norte\nTipo: Kiosco","raw_payload":{}}), content_type="application/json")

        def post(pid, text):
            r = client.post(url, data=json.dumps({"provider":"whatsapp_mock","provider_message_id":f"{pid}_{wh}","whatsapp_id":wh,"text":text,"raw_payload":{}}), content_type="application/json")
            reply = getattr(r, "json", lambda: {})().get("reply")
            print(f"{text} -> {reply}")
            return reply

        post("t3_e2", "+ DEMO-001 3")
        post("t3_e3", "= DEMO-001 5")
        post("t3_e4", "- DEMO-002")
        post("t3_c1", "OK")
        post("t3_c2", "OK")
        post("t3_e5", "+ DEMO-003 2")
