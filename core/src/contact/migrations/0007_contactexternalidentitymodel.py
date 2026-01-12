from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('contact', '0006_messageeventlogmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactExternalIdentityModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider', models.CharField(max_length=32)),
                ('external_id', models.CharField(max_length=128)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='external_identities', to='contact.contact')),
            ],
            options={
                'unique_together': {('provider', 'external_id')},
            },
        ),
    ]

