# Generated by Django 5.1.5 on 2025-02-02 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_alter_payment_payment_method_alter_payment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('pending', 'PENDING'), ('done', 'DONE'), ('fail', 'FAIL'), ('refunded', 'REFUNDED')], default='pending', max_length=100),
        ),
    ]
