from django.test import TestCase
from contact.models import Contact, OrderModel, ConversationStateModel
from contact.modules.conversations.infrastructure.orm import contact_repo, conversation_repo
from contact.modules.conversations.domain.conversation_stage import ConversationStage
from contact.modules.orders.application.commands.create_order_proposal_cmd import execute as create_order_proposal
from contact.modules.orders.application.templates.kiosk_template import get_kiosk_template, _validate
from contact.shared.domain.errors import InvalidTemplateItem
from contact.shared.infrastructure.uow import UnitOfWork


class Task1VerticalSliceTests(TestCase):
    def setUp(self):
        self.whatsapp_id = "+5493510000000"
        self.name = "Kiosco Demo"
        self.zone = "Centro"
        self.business_type = "Kiosco"

    def test_upsert_contact_and_state_created(self):
        c = contact_repo.upsert_minimal(self.whatsapp_id, self.name, self.zone, self.business_type)
        self.assertIsNotNone(c.id)
        st = conversation_repo.set_stage_and_last_order(c.id, ConversationStage.E1_MIN_DATA, None)
        self.assertEqual(st.stage, ConversationStage.E1_MIN_DATA.value)

    def test_create_order_proposal_creates_order_items_and_sets_stage_E2(self):
        contact_repo.upsert_minimal(self.whatsapp_id, self.name, self.zone, self.business_type)
        oid = create_order_proposal(self.whatsapp_id)
        order = OrderModel.objects.get(id=oid)
        self.assertEqual(order.status, "PROPOSED")
        self.assertTrue(10 <= order.items.count() <= 15)
        st = ConversationStateModel.objects.get(contact_id=order.contact_id)
        self.assertEqual(st.stage, ConversationStage.E2_PROPOSAL.value)
        self.assertEqual(st.last_order_id, order.id)

    def test_uow_rolls_back_on_error(self):
        c = contact_repo.upsert_minimal(self.whatsapp_id, self.name, self.zone, self.business_type)
        before = OrderModel.objects.count()
        try:
            with UnitOfWork() as uow:
                items = get_kiosk_template()
                o = uow.orders.create_proposed(c.id, items)
                raise RuntimeError("forced")
        except RuntimeError:
            pass
        after = OrderModel.objects.count()
        self.assertEqual(before, after)

    def test_set_stage_E2_requires_last_order(self):
        c = contact_repo.upsert_minimal(self.whatsapp_id, self.name, self.zone, self.business_type)
        with self.assertRaises(ValueError):
            conversation_repo.set_stage_and_last_order(c.id, ConversationStage.E2_PROPOSAL, None)

    def test_invalid_template_item_details(self):
        bad_items = [{"product_ref": "SKU:coca", "qty": 0}] * 10
        with self.assertRaises(InvalidTemplateItem) as ctx:
            _validate(bad_items)
        msg = str(ctx.exception)
        self.assertIn("ref=SKU:coca", msg)
        self.assertIn("qty=0", msg)
