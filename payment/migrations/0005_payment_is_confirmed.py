# Generated by Django 4.2 on 2024-03-08 19:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("payment", "0004_alter_payment_amount"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="is_confirmed",
            field=models.BooleanField(default=False, verbose_name="Подтвержден"),
        ),
    ]
