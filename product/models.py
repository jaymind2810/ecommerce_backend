from __future__ import unicode_literals
from django.db import models
from account.models import User
from datetime import datetime
import random


# Create your models here.

class Category(models.Model):

    name = models.CharField(max_length=128)
    description = models.TextField()
    cat_photo = models.ImageField(upload_to='category/', blank=True)

    create_date = models.DateTimeField(auto_now_add=True, editable=False, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, editable=False, blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    publish_choices = [
        ('Published', 'Published'),
        ('Scheduled', 'Scheduled'),
        ('Draft', 'Draft'),
    ]

    visibility_choices = [
        ('Public', 'Public'),
        ('Hidden', 'Hidden'),
    ]

    name = models.CharField(max_length=128)
    short_text = models.CharField(max_length=128)
    description = models.TextField()
    amount = models.CharField(default="1", max_length=10)
    product_photo = models.ImageField(upload_to='products/', blank=True, default='products/img-6.png')
    product_photo_1 = models.ImageField(upload_to='products/', blank=True)

    # date = models.CharField(max_length=15)
    # time = models.CharField(max_length=12, default="00:00")
    # act = models.IntegerField(default=0)
    # rand = models.IntegerField(default=0)

    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    manufacturer_name = models.CharField(max_length=128, blank=True)
    manufacturer_brand = models.CharField(max_length=128, blank=True)
    product_stock = models.CharField(max_length=128, blank=True)
    product_price = models.CharField(max_length=128, blank=True)
    publish_status = models.CharField(choices=publish_choices, default='Draft', max_length=15)
    visibility = models.CharField(choices=visibility_choices, default='Draft', max_length=15)

    last_published_date_time = models.DateTimeField(blank=True, null=True)

    create_by = models.CharField(max_length=128, default="-")
    create_date = models.DateTimeField(auto_now_add=True, editable=False, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, editable=False, blank=True, null=True)

    def generate_product_sequence():
        prefix = "PRO"
        current_time = datetime.now().strftime('%y%m%d%H%M%S')[:6]  # Extract part of timestamp
        random_suffix = str(random.randint(10000, 99999))  # Generate random 5-digit number
        return f"{prefix}{current_time}{random_suffix}"

    product_sequence = models.CharField(default=generate_product_sequence, max_length=15)

    def __str__(self):
        return self.name


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='products/', null=True, blank=True)


class Comment(models.Model):
    user_id = models.ForeignKey('account.User', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    description = models.TextField()
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True, editable=False, blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, editable=False, blank=True, null=True)

    def __str__(self):
        return self.name
