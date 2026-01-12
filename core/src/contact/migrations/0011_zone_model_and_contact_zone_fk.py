from django.db import migrations, models
import django.db.models.deletion


CPC_ZONES = [
    ("CPC_01_CENTRO_AMERICA", "CPC 1 — Centro América"),
    ("CPC_02_MONSEÑOR_PABLO_CABRERA", "CPC 2 — Monseñor Pablo Cabrera"),
    ("CPC_03_ARGÜELLO", "CPC 3 — Argüello"),
    ("CPC_04_COLÓN", "CPC 4 — Colón"),
    ("CPC_05_RUTA_20", "CPC 5 — Ruta 20"),
    ("CPC_06_VILLA_EL_LIBERTADOR", "CPC 6 — Villa El Libertador"),
    ("CPC_07_EMPALME", "CPC 7 — Empalme"),
    ("CPC_08_PUEYRREDÓN", "CPC 8 — Pueyrredón"),
    ("CPC_09_RANCAGUA", "CPC 9 — Rancagua"),
    ("CPC_10_MERCADO_DE_LA_CIUDAD", "CPC 10 — Mercado de la Ciudad"),
    ("CPC_11_GUIÑAZÚ", "CPC 11 — Guiñazú"),
]


def seed_cpc_zones(apps, schema_editor):
    ZoneModel = apps.get_model("contact", "ZoneModel")
    for code, name in CPC_ZONES:
        ZoneModel.objects.get_or_create(code=code, defaults={"name": name, "is_active": True})


def unseed_cpc_zones(apps, schema_editor):
    ZoneModel = apps.get_model("contact", "ZoneModel")
    for code, _ in CPC_ZONES:
        ZoneModel.objects.filter(code=code).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("contact", "0010_add_review_deadline_at"),
    ]

    operations = [
        migrations.CreateModel(
            name="ZoneModel",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=64, unique=True)),
                ("name", models.CharField(max_length=255)),
                ("is_dangerous", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name="contact",
            name="zone",
        ),
        migrations.AddField(
            model_name="contact",
            name="zone",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="contacts", to="contact.zonemodel"),
        ),
        migrations.RunPython(seed_cpc_zones, reverse_code=unseed_cpc_zones),
    ]

