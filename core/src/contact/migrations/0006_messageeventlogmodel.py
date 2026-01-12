from django.db import migrations, models
import django.db.models.deletion
from django.utils import timezone
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        ('contact', '0005_contactreorderprofilemodel_contactfactmodel_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageEventLogModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider', models.CharField(max_length=32)),
                ('direction', models.CharField(max_length=8)),
                ('external_event_id', models.CharField(blank=True, max_length=128, null=True)),
                ('echo_id', models.CharField(blank=True, max_length=128, null=True)),
                ('conversation_external_id', models.CharField(max_length=128)),
                ('status', models.CharField(max_length=16)),
                ('payload_json', models.JSONField()),
                ('created_at', models.DateTimeField(default=timezone.now)),
                ('contact', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='message_events', to='contact.contact')),
            ],
        ),
        migrations.AddConstraint(
            model_name='messageeventlogmodel',
            constraint=models.UniqueConstraint(fields=('provider', 'external_event_id'), name='uniq_inbound_provider_event'),
        ),
        migrations.AddConstraint(
            model_name='messageeventlogmodel',
            constraint=models.UniqueConstraint(fields=('provider', 'echo_id'), name='uniq_outbound_provider_echo'),
        ),
    ]

