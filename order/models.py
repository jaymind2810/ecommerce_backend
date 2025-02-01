from django.db import models
from account.models import User
from product.models import Product
from checkout.models import Address

class Order(models.Model):
    
    customer = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='orders')  # User who placed the order
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of order creation
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp of last update

    # Order status and tracking
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirm', 'Confirm'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('returned', 'Returned'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    tracking_number = models.CharField(max_length=50, blank=True, null=True) 

    # Billing and shipping information
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)

    # Payment details
    payment_method = models.CharField(max_length=50)  # Can be extended to include a ForeignKey to a Payment model for more complex scenarios
    payment_confirmed = models.BooleanField(default=False)

    amount_pay = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    # Order items
    # items = models.ManyToManyField('OrderItem', through='OrderItemThrough')


    # def __str__(self):
    #     return f"Order #{self.order_id} - {self.customer.username} ({self.status})"

class OrderItem(models.Model):
    """
    Model for representing individual items within an order.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)  # Link to your product model
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total_price(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.product.name} (x{self.quantity}) - {self.order.id}"
