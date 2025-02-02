from decimal import Decimal
from django.db import models
from account.models import User
from order.models import Order 

# Create your models here.

class Payment(models.Model):

    PAYMENT_STATUS_CHOICES = (
        ("pending", "PENDING"), 
        ("done", "DONE"), 
        ("fail", "FAIL"), 
        ('refunded', 'REFUNDED'),
    )

    PAYMENT_METHOD_CHOICES = (
        ("stripe", "Stripe"), 
        ("payPal", "PayPal"), 
        ("cod", "Cash on Delivery")
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_id = models.CharField(default="-", max_length=28)
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment", null=True)
    
    payment_method = models.CharField(max_length=100, choices=PAYMENT_METHOD_CHOICES, default="cod")
    transaction_id = models.CharField(blank=True, null=True, max_length=128)
    payment_method_id = models.CharField(blank=True, null=True, max_length=128)
    
    status = models.CharField(max_length=100, choices=PAYMENT_STATUS_CHOICES, default="pending")

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)

    is_promocode_used = models.BooleanField(default=False)
    promocode_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))

    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




