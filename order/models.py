from django.db import models
from account.models import User
from product.models import Product

class Order(models.Model):
    
    # Order identification and metadata
    order_id = models.CharField(max_length=50, unique=True, primary_key=True)
    customer = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='orders')  # User who placed the order
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of order creation
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp of last update

    # Order status and tracking
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('returned', 'Returned'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    tracking_number = models.CharField(max_length=50, blank=True, null=True)  # Optional tracking number

    # Billing and shipping information
    billing_address = models.TextField()  # Can be structured with separate fields for street address, city, state, etc.
    shipping_address = models.TextField()  # Can be structured with separate fields for better organization

    # Payment details
    payment_method = models.CharField(max_length=50)  # Can be extended to include a ForeignKey to a Payment model for more complex scenarios
    payment_confirmed = models.BooleanField(default=False)

    # Order items
    # items = models.ManyToManyField('OrderItem', through='OrderItemThrough')


    def __str__(self):
        return f"Order #{self.order_id} - {self.customer.username} ({self.status})"

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
        return f"{self.product.name} (x{self.quantity}) - {self.order.order_id}"

# class OrderItemThrough(models.Model):
#     """
#     Through model for order-item relationship (optional for customization).
#     """
#     order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
#     order_item_id = models.ForeignKey(OrderItem, on_delete=models.CASCADE)

#     class Meta:
#         unique_together = (('order_id', 'order_item_id'),)  # Ensure only one entry per order-item combination
