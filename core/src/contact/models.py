from django.db import models

class Contact(models.Model):
    TYPE_SUPPLIER = "supplier"
    TYPE_CLIENT = "client"
    TYPE_INTERNAL = "internal"
    
    whatsapp_id = models.CharField(max_length=64, unique=True, null=True, blank=True)
    name = models.CharField(max_length=255)
    zone = models.CharField(max_length=128, default="")
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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
