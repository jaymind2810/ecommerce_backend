# Generated by Django 5.1.5 on 2025-02-02 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_delete',
            field=models.BooleanField(default=False),
        ),
    ]
