from django.core.management.base import BaseCommand
from contact.modules.conversations.infrastructure.orm import contact_repo, conversation_repo
from contact.modules.conversations.domain.conversation_stage import ConversationStage
from contact.modules.orders.application.commands.create_order_proposal_cmd import execute as create_order_proposal
from contact.modules.orders.application.queries.get_order_summary_q import execute as get_summary


class Command(BaseCommand):
    help = "Demo Tarea 1: upsert contacto, propuesta de pedido y resumen"

    def add_arguments(self, parser):
        parser.add_argument("--whatsapp", required=True)
        parser.add_argument("--name", required=True)
        parser.add_argument("--zone", required=True)
        parser.add_argument("--type", dest="business_type", required=True)

    def handle(self, *args, **opts):
        whatsapp = opts["whatsapp"]
        name = opts["name"]
        zone = opts["zone"]
        business_type = opts["business_type"]

        c = contact_repo.upsert_minimal(whatsapp, name, zone, business_type)
        conversation_repo.set_stage_and_last_order(c.id, ConversationStage.E1_MIN_DATA, None)
        order_id = create_order_proposal(whatsapp)
        summary = get_summary(order_id)
        self.stdout.write(self.style.SUCCESS(f"Order {order_id} created"))
        self.stdout.write(str(summary))

