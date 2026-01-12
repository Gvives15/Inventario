from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.contrib import admin
from contact.models import Contact, OrderModel, ZoneModel
from contact.admin import ZoneFilter, OrderAdmin
 
class DummyModelAdmin(admin.ModelAdmin):
    pass
 
class AdminZoneFilterTests(TestCase):
    def setUp(self):
        self.zone_a = ZoneModel.objects.create(code="CPC_03_ARGUELLO", name="CPC 3 — Argüello")
        self.zone_b = ZoneModel.objects.create(code="CPC_04_COLON", name="CPC 4 — Colón")
        self.contact_a = Contact.objects.create(name="Cliente A", type=Contact.TYPE_CLIENT, zone=self.zone_a)
        self.contact_b = Contact.objects.create(name="Cliente B", type=Contact.TYPE_CLIENT)
        self.order_a = OrderModel.objects.create(contact=self.contact_a, status="CONFIRMED", ops_status=OrderModel.OPS_REQUIRES_REVIEW)
        self.order_b = OrderModel.objects.create(contact=self.contact_b, status="CONFIRMED", ops_status=OrderModel.OPS_REQUIRES_REVIEW)
        self.site = AdminSite()
        self.ma = DummyModelAdmin(OrderModel, self.site)
 
    def _filter(self, val=None):
        rf = ZoneFilter(self.site, {}, OrderModel, self.ma)
        rf.used_parameters = {}
        rf.value = lambda: val
        return rf
 
    def test_zone_lookups_show_only_zones_with_contacts(self):
        rf = self._filter()
        lookups = rf.lookups(None, self.ma)
        names = set(name for _, name in lookups)
        self.assertIn("CPC 3 — Argüello", names)
        self.assertNotIn("CPC 4 — Colón", names)
 
    def test_zone_queryset_filters_orders_by_zone(self):
        rf = self._filter(str(self.zone_a.id))
        qs = rf.queryset(None, OrderModel.objects.all())
        ids = set(qs.values_list("id", flat=True))
        self.assertIn(self.order_a.id, ids)
        self.assertNotIn(self.order_b.id, ids)

    def test_zone_queryset_filters_contacts_by_zone(self):
        ma_contact = DummyModelAdmin(Contact, self.site)
        rf = ZoneFilter(self.site, {}, Contact, ma_contact)
        rf.used_parameters = {}
        rf.value = lambda: str(self.zone_a.id)
        
        qs = rf.queryset(None, Contact.objects.all())
        ids = set(qs.values_list("id", flat=True))
        self.assertIn(self.contact_a.id, ids)
        self.assertNotIn(self.contact_b.id, ids)
