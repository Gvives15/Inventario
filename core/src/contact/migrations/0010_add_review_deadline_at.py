from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("contact", "0009_ops_status_and_ops_event"),
    ]

    operations = [
        migrations.AddField(
            model_name="ordermodel",
            name="review_deadline_at",
            field=models.DateTimeField(null=True, blank=True, db_index=True),
        ),
    ]
