# Generated by Django 5.1.5 on 2025-02-02 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0006_alter_payment_promocode_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='is_delete',
            field=models.BooleanField(default=False),
        ),
    ]
