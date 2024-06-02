from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    """
    Inline admin for displaying order items within the Order admin view.
    """
    model = OrderItem
    readonly_fields = ('product', 'unit_price',)
    # readonly_fields = ('product', 'unit_price', 'get_total_price')

class OrderAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Order model.
    """
    inlines = [OrderItemInline]
    list_display = ('order_id', 'customer', 'status', 'created_at', 'get_total_amount')  # Add a custom method for total amount
    list_filter = ('status', 'created_at')
    search_fields = ('order_id', 'customer__username')  # Search by order ID and customer username

    def get_total_amount(self, obj):
        """
        Calculates the total amount of the order by summing the prices of all order items.
        """
        total = sum(item.get_total_price() for item in obj.order_items.all())
        return total


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem) 