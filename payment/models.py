from django.db import models
from account.models import User 

# Create your models here.

class Payment(models.Model):

    payment_status_action = (("DRAFT", "DRAFT"), ("PENDING", "PENDING"), ("DONE", "DONE"), ("FAIL", "FAIL"))

    payment_method_choices = (("Stripe", "Stripe"), ("PayPal", "PayPal"))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_refrence_id = models.CharField(blank=True, null=True, max_length=128)
    status = models.CharField(max_length=100, choices=payment_status_action, default="DRAFT")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)

    is_promocode_used = models.BooleanField(default=False)
    promocode_amount = models.CharField(default='0')

    payment_method = models.CharField(max_length=100, choices=payment_method_choices, default="Stripe")
    customer_id = models.CharField(default="-", max_length=28)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# class OrderItems(models.Model):

#     payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
#     box = models.ForeignKey(Box, on_delete=models.CASCADE)
#     promo_code = models.ForeignKey(PromoCodes, blank=True, null=True, on_delete=models.PROTECT)
#     is_promocode_used = models.BooleanField(default=False)
#     quantity = models.PositiveIntegerField(default=1)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)




