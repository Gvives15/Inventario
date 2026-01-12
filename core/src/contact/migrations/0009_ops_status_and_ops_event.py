from django.db import migrations, models

OPS_CONFIRMED = "CONFIRMED"

def backfill_ops_status(apps, schema_editor):
    OrderModel = apps.get_model("contact", "OrderModel")
    OrderModel.objects.filter(ops_status__isnull=True, status="CONFIRMED").update(ops_status=OPS_CONFIRMED)

class Migration(migrations.Migration):

    dependencies = [
        ("contact", "0008_contactreorderprofilemodel_postpone_confidence_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="ordermodel",
            name="ops_status",
            field=models.CharField(choices=[
                ("CONFIRMED", "CONFIRMED"),
                ("REQUIRES_REVIEW", "REQUIRES_REVIEW"),
                ("PREPARING", "PREPARING"),
                ("READY", "READY"),
                ("OUT_FOR_DELIVERY", "OUT_FOR_DELIVERY"),
                ("DELIVERED", "DELIVERED"),
                ("PAID", "PAID"),
                ("CANCELLED", "CANCELLED"),
                ("REPLACED", "REPLACED"),
            ], db_index=True, max_length=32, null=True, blank=True),
        ),
        migrations.AddField(
            model_name="ordermodel",
            name="review_reason_code",
            field=models.CharField(choices=[
                ("SKU_UNKNOWN", "SKU_UNKNOWN"),
                ("CHANGE_AFTER_CONFIRM", "CHANGE_AFTER_CONFIRM"),
                ("CANCEL_AFTER_CONFIRM", "CANCEL_AFTER_CONFIRM"),
                ("ORDER_REPLACED", "ORDER_REPLACED"),
                ("ADDRESS_OUT_OF_ZONE", "ADDRESS_OUT_OF_ZONE"),
                ("CUSTOMER_NOT_AVAILABLE", "CUSTOMER_NOT_AVAILABLE"),
                ("PAYMENT_ISSUE", "PAYMENT_ISSUE"),
                ("MANUAL_REVIEW", "MANUAL_REVIEW"),
            ], db_index=True, max_length=64, null=True, blank=True),
        ),
        migrations.AddField(
            model_name="ordermodel",
            name="review_reason_note",
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name="ordermodel",
            name="ops_notes",
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name="ordermodel",
            name="ops_updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name="OrderOpsEventModel",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("from_status", models.CharField(max_length=32)),
                ("to_status", models.CharField(max_length=32)),
                ("note", models.TextField(null=True, blank=True)),
                ("review_reason_code", models.CharField(max_length=64, null=True, blank=True)),
                ("review_reason_note", models.TextField(null=True, blank=True)),
                ("at", models.DateTimeField(auto_now_add=True)),
                ("order", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="ops_events", to="contact.ordermodel")),
            ],
            options={
                "ordering": ["-at", "-id"],
            },
        ),
        migrations.AddIndex(
            model_name="orderopseventmodel",
            index=models.Index(fields=["order", "at"], name="order_op_at_idx"),
        ),
        migrations.RunPython(backfill_ops_status, migrations.RunPython.noop),
    ]

