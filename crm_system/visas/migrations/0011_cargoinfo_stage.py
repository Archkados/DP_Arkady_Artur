# Generated by Django 5.0.4 on 2025-03-03 10:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("visas", "0010_trackingrequest_departure_date_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="CargoInfo",
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
                (
                    "name",
                    models.CharField(max_length=255, verbose_name="Название груза"),
                ),
                (
                    "file",
                    models.FileField(upload_to="cargo_files/", verbose_name="Файл"),
                ),
                (
                    "tracking_request",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cargo_infos",
                        to="visas.trackingrequest",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Stage",
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
                (
                    "name",
                    models.CharField(max_length=255, verbose_name="Название этапа"),
                ),
                (
                    "tracking_request",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="stages",
                        to="visas.trackingrequest",
                    ),
                ),
            ],
        ),
    ]
