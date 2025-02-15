# Generated by Django 5.1.5 on 2025-02-02 07:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='payment_refrence_id',
            new_name='transaction_id',
        ),
        migrations.AddField(
            model_name='payment',
            name='order',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='order.order'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(choices=[('Stripe', 'Stripe'), ('PayPal', 'PayPal'), ('Cod', 'Cash on Delivery')], default='Stripe', max_length=100),
        ),
        migrations.AlterField(
            model_name='payment',
            name='promocode_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('DONE', 'DONE'), ('FAIL', 'FAIL'), ('REFUNDED', 'REFUNDED')], default='PENDING', max_length=100),
        ),
    ]
