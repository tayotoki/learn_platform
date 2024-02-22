# Generated by Django 4.2 on 2024-02-22 09:38

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="phone_number",
            field=phonenumber_field.modelfields.PhoneNumberField(
                blank=True,
                max_length=128,
                null=True,
                region=None,
                verbose_name="Телефон",
            ),
        ),
    ]
