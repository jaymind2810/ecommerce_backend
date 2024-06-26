# Generated by Django 5.0.6 on 2024-05-30 17:50

import django.db.models.deletion
import product.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('cat_photo', models.ImageField(blank=True, upload_to='category/')),
                ('create_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('short_text', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('amount', models.CharField(default='1', max_length=10)),
                ('product_photo', models.ImageField(blank=True, default='products/img-6.png', upload_to='products/')),
                ('product_photo_1', models.ImageField(blank=True, upload_to='products/')),
                ('date', models.CharField(max_length=15)),
                ('time', models.CharField(default='00:00', max_length=12)),
                ('act', models.IntegerField(default=0)),
                ('rand', models.IntegerField(default=0)),
                ('manufacturer_name', models.CharField(blank=True, max_length=128)),
                ('manufacturer_brand', models.CharField(blank=True, max_length=128)),
                ('product_stock', models.CharField(blank=True, max_length=128)),
                ('product_price', models.CharField(blank=True, max_length=128)),
                ('publish_status', models.CharField(choices=[('Published', 'Published'), ('Scheduled', 'Scheduled'), ('Draft', 'Draft')], default='Draft', max_length=15)),
                ('visibility', models.CharField(choices=[('Public', 'Public'), ('Hidden', 'Hidden')], default='Draft', max_length=15)),
                ('last_published_date_time', models.DateTimeField(blank=True, null=True)),
                ('create_by', models.CharField(default='-', max_length=128)),
                ('create_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
                ('product_sequence', models.CharField(default=product.models.Product.generate_product_sequence, max_length=15)),
                ('category_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.category')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('email', models.CharField(max_length=128)),
                ('title', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('create_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, null=True)),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
    ]
