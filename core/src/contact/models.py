from django.db import models
 
class ZoneModel(models.Model):
    code = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=255)
    is_dangerous = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return self.name

class Contact(models.Model):
    TYPE_SUPPLIER = "supplier"
    TYPE_CLIENT = "client"
    TYPE_INTERNAL = "internal"
    
    whatsapp_id = models.CharField(max_length=64, unique=True, null=True, blank=True)
    name = models.CharField(max_length=255)
    zone = models.ForeignKey(ZoneModel, null=True, blank=True, on_delete=models.SET_NULL, related_name="contacts")
    business_type = models.CharField(max_length=128, default="")
    type = models.CharField(
        max_length=20,
        choices=[
            (TYPE_SUPPLIER, "Proveedor"),
            (TYPE_CLIENT, "Cliente"),
            (TYPE_INTERNAL, "Ubicación Interna"),
        ]
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class OrderModel(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=16)
    OPS_CONFIRMED = "CONFIRMED"
    OPS_REQUIRES_REVIEW = "REQUIRES_REVIEW"
    OPS_PREPARING = "PREPARING"
    OPS_READY = "READY"
    OPS_OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    OPS_DELIVERED = "DELIVERED"
    OPS_PAID = "PAID"
    OPS_CANCELLED = "CANCELLED"
    OPS_REPLACED = "REPLACED"
    OPS_STATUS_CHOICES = [
        (OPS_CONFIRMED, OPS_CONFIRMED),
        (OPS_REQUIRES_REVIEW, OPS_REQUIRES_REVIEW),
        (OPS_PREPARING, OPS_PREPARING),
        (OPS_READY, OPS_READY),
        (OPS_OUT_FOR_DELIVERY, OPS_OUT_FOR_DELIVERY),
        (OPS_DELIVERED, OPS_DELIVERED),
        (OPS_PAID, OPS_PAID),
        (OPS_CANCELLED, OPS_CANCELLED),
        (OPS_REPLACED, OPS_REPLACED),
    ]
    ops_status = models.CharField(max_length=32, null=True, blank=True, choices=OPS_STATUS_CHOICES, db_index=True)
    REVIEW_SKU_UNKNOWN = "SKU_UNKNOWN"
    REVIEW_CHANGE_AFTER_CONFIRM = "CHANGE_AFTER_CONFIRM"
    REVIEW_CANCEL_AFTER_CONFIRM = "CANCEL_AFTER_CONFIRM"
    REVIEW_ORDER_REPLACED = "ORDER_REPLACED"
    REVIEW_ADDRESS_OUT_OF_ZONE = "ADDRESS_OUT_OF_ZONE"
    REVIEW_CUSTOMER_NOT_AVAILABLE = "CUSTOMER_NOT_AVAILABLE"
    REVIEW_PAYMENT_ISSUE = "PAYMENT_ISSUE"
    REVIEW_MANUAL = "MANUAL_REVIEW"
    REVIEW_CODE_CHOICES = [
        (REVIEW_SKU_UNKNOWN, REVIEW_SKU_UNKNOWN),
        (REVIEW_CHANGE_AFTER_CONFIRM, REVIEW_CHANGE_AFTER_CONFIRM),
        (REVIEW_CANCEL_AFTER_CONFIRM, REVIEW_CANCEL_AFTER_CONFIRM),
        (REVIEW_ORDER_REPLACED, REVIEW_ORDER_REPLACED),
        (REVIEW_ADDRESS_OUT_OF_ZONE, REVIEW_ADDRESS_OUT_OF_ZONE),
        (REVIEW_CUSTOMER_NOT_AVAILABLE, REVIEW_CUSTOMER_NOT_AVAILABLE),
        (REVIEW_PAYMENT_ISSUE, REVIEW_PAYMENT_ISSUE),
        (REVIEW_MANUAL, REVIEW_MANUAL),
    ]
    review_reason_code = models.CharField(max_length=64, null=True, blank=True, choices=REVIEW_CODE_CHOICES, db_index=True)
    review_reason_note = models.TextField(null=True, blank=True)
    review_deadline_at = models.DateTimeField(null=True, blank=True, db_index=True)
    ops_notes = models.TextField(null=True, blank=True)
    ops_updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def items_count(self) -> int:
        return self.items.aggregate(models.Sum("qty")).get("qty__sum") or 0


class OrderItemModel(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name="items")
    product_ref = models.CharField(max_length=128)
    qty = models.PositiveIntegerField()


class ConversationStateModel(models.Model):
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE, related_name="conversation_state")
    stage = models.CharField(max_length=32)
    last_order = models.ForeignKey(OrderModel, null=True, blank=True, on_delete=models.SET_NULL)
    updated_at = models.DateTimeField(auto_now=True)


class MessageInboundModel(models.Model):
    provider = models.CharField(max_length=64)
    provider_message_id = models.CharField(max_length=128)
    whatsapp_id = models.CharField(max_length=64)
    text = models.TextField()
    raw_payload = models.TextField()
    received_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("provider", "provider_message_id")

# Import hub: register contact history models
from contact.modules.contacts.infrastructure.orm.contact_history_models import (
    ContactFactModel,
    ContactTagModel,
    ContactSkuStatModel,
    ContactReorderProfileModel,
)
from contact.modules.messaging.infrastructure.orm.message_event_models import (
    MessageEventLogModel,
)
class OrderOpsEventModel(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name="ops_events")
    from_status = models.CharField(max_length=32)
    to_status = models.CharField(max_length=32)
    note = models.TextField(null=True, blank=True)
    review_reason_code = models.CharField(max_length=64, null=True, blank=True)
    review_reason_note = models.TextField(null=True, blank=True)
    at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-at", "-id"]
        indexes = [
            models.Index(fields=["order", "at"]),
        ]


class OrderReviewQueue(OrderModel):
    class Meta:
        proxy = True
        verbose_name = "Review Queue"
        verbose_name_plural = "Review Queue"
