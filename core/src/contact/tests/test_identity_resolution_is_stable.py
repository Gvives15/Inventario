from django.test import TestCase
from contact.modules.contacts.application.commands.resolve_chatwoot_identity_cmd import execute as resolve_identity
from contact.models import Contact


class IdentityResolutionTests(TestCase):
    def test_same_external_identity_maps_to_same_contact(self):
        cid1 = resolve_identity("ext-1", "conv-1")
        cid2 = resolve_identity("ext-1", "conv-2")
        self.assertEqual(cid1, cid2)
        c = Contact.objects.get(id=cid1)
        self.assertTrue(c.whatsapp_id.startswith("chatwoot:"))
