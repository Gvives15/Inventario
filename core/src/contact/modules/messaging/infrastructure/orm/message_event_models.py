from django.db import models
from django.utils import timezone
from contact.models import Contact


class MessageEventLogModel(models.Model):
    provider = models.CharField(max_length=32)
    direction = models.CharField(max_length=8)
    external_event_id = models.CharField(max_length=128, null=True, blank=True)
    echo_id = models.CharField(max_length=128, null=True, blank=True)
    conversation_external_id = models.CharField(max_length=128)
    contact = models.ForeignKey(Contact, null=True, blank=True, on_delete=models.SET_NULL, related_name="message_events")
    status = models.CharField(max_length=16)
    payload_json = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["provider", "external_event_id"], name="uniq_inbound_provider_event"),
            models.UniqueConstraint(fields=["provider", "echo_id"], name="uniq_outbound_provider_echo"),
        ]
