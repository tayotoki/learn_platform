# Generated by Django 4.2 on 2024-02-22 11:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("payment", "0002_alter_payment_content_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="amount",
            field=models.DecimalField(decimal_places=2, max_digits=8, verbose_name="Сумма оплаты"),
        ),
    ]
