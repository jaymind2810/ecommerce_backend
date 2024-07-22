from django.db import models
from account.models import User
from product.models import Product
import datetime

# Create your models here.


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'user',)


class Address(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20,default="-")
    email = models.CharField(max_length=20, default="-")
    is_delete = models.BooleanField(max_length=20, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.street}, {self.city}, {self.state}, {self.country}, {self.postal_code}'

