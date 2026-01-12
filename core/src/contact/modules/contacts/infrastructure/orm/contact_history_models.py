from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

from contact.models import Contact, OrderItemModel


class ContactFactModel(models.Model):
    SOURCE_USER = "USER"
    SOURCE_SYSTEM = "SYSTEM"
    SOURCE_AI = "AI"
    SOURCE_IMPORT = "IMPORT"

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="facts")
    key = models.CharField(max_length=64)
    value_json = models.JSONField()
    confidence = models.FloatField(default=1.0)
    source = models.CharField(
        max_length=16,
        choices=[
            (SOURCE_USER, SOURCE_USER),
            (SOURCE_SYSTEM, SOURCE_SYSTEM),
            (SOURCE_AI, SOURCE_AI),
            (SOURCE_IMPORT, SOURCE_IMPORT),
        ],
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("contact", "key")


class ContactTagModel(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="tags")
    tag = models.CharField(max_length=64)
    confidence = models.FloatField(default=1.0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("contact", "tag")


class ContactSkuStatModel(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="sku_stats")
    sku = models.CharField(max_length=128)

    orders_count = models.PositiveIntegerField(default=0)
    qty_total = models.PositiveIntegerField(default=0)
    qty_last = models.PositiveIntegerField(default=0)
    qty_avg = models.FloatField(default=0.0)

    first_ordered_at = models.DateTimeField(null=True, blank=True)
    last_ordered_at = models.DateTimeField(null=True, blank=True)

    score = models.FloatField(default=0.0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("contact", "sku")

    def clean(self):
        # Guardar por si alguien intenta crear stats con SKU inválido
        if self.sku.isdigit() or len(self.sku) < 3:
            raise ValidationError("Invalid SKU for stats")


class ContactReorderProfileModel(models.Model):
    STATUS_ACTIVE = "ACTIVE"
    STATUS_PAUSED = "PAUSED"
    POSTPONE_PENDING = "PENDING"
    POSTPONE_APPLIED = "APPLIED"
    POSTPONE_REJECTED = "REJECTED"

    contact = models.OneToOneField(Contact, on_delete=models.CASCADE, related_name="reorder_profile")
    status = models.CharField(
        max_length=16,
        choices=[
            (STATUS_ACTIVE, STATUS_ACTIVE),
            (STATUS_PAUSED, STATUS_PAUSED),
        ],
        default=STATUS_ACTIVE,
    )
    cadence_days = models.PositiveIntegerField(null=True, blank=True)
    preferred_weekdays = models.JSONField(null=True, blank=True)
    next_reorder_date = models.DateField(null=True, blank=True)
    default_list_code = models.CharField(max_length=64, default="kiosk_base")
    updated_at = models.DateTimeField(auto_now=True)
    postpone_raw_text = models.TextField(null=True, blank=True)
    postpone_until_dt = models.DateTimeField(null=True, blank=True)
    postpone_window = models.CharField(max_length=64, null=True, blank=True)
    postpone_confidence = models.FloatField(default=0.0)
    postpone_status = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        choices=[
            (POSTPONE_PENDING, POSTPONE_PENDING),
            (POSTPONE_APPLIED, POSTPONE_APPLIED),
            (POSTPONE_REJECTED, POSTPONE_REJECTED),
        ],
    )
    postpone_created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
