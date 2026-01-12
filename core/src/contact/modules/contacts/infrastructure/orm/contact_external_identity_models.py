from django.db import models
from contact.models import Contact


class ContactExternalIdentityModel(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="external_identities")
    provider = models.CharField(max_length=32)
    external_id = models.CharField(max_length=128)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("provider", "external_id")

