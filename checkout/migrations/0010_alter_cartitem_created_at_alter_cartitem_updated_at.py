# Generated by Django 5.0.2 on 2024-07-20 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0009_cartitem_created_at_cartitem_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
