# Generated by Django 4.2.11 on 2024-07-12 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_product_short_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_photo_1',
        ),
    ]