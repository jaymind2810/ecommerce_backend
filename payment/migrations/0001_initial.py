# Generated by Django 5.0.2 on 2024-07-27 05:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_refrence_id', models.CharField(blank=True, max_length=128, null=True)),
                ('status', models.CharField(choices=[('DRAFT', 'DRAFT'), ('PENDING', 'PENDING'), ('DONE', 'DONE'), ('FAIL', 'FAIL')], default='DRAFT', max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(max_length=10)),
                ('is_promocode_used', models.BooleanField(default=False)),
                ('promocode_amount', models.CharField(default='0')),
                ('payment_method', models.CharField(choices=[('Stripe', 'Stripe'), ('PayPal', 'PayPal')], default='Stripe', max_length=100)),
                ('customer_id', models.CharField(default='-', max_length=28)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
