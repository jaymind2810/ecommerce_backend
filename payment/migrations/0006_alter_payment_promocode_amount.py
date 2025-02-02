# Generated by Django 5.1.5 on 2025-02-02 13:31

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_payment_payment_method_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='promocode_amount',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10),
        ),
    ]
