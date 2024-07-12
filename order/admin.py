from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    
    model = OrderItem
    readonly_fields = ('unit_price',)
    extra = 1
    # readonly_fields = ('product', 'unit_price', 'get_total_price')
    
    def get_total_item_amount(self, obj):
        """
        Calculates the total amount of the order by summing the prices of all order items.
        """
        total = sum(item.get_total_price() for item in obj.order_items.all())
        return total


class OrderAdmin(admin.ModelAdmin):
    
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