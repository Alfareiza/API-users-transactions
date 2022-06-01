# Generated by Django 4.0.4 on 2022-05-27 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("reference", models.CharField(max_length=6, unique=True)),
                ("date", models.DateField()),
                (
                    "type",
                    models.CharField(
                        choices=[("outflow", "Outflow"), ("inflow", "Inflow")],
                        default="outflow",
                        max_length=10,
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(decimal_places=2, max_digits=12),
                ),
                ("category", models.CharField(max_length=15)),
                ("user_email", models.EmailField(max_length=254)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ("-date",),
            },
        ),
    ]
