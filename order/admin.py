from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    
    model = OrderItem
    # readonly_fields = ('unit_price',)
    extra = 1
    # readonly_fields = ('product', 'unit_price', 'get_total_price') 


class OrderAdmin(admin.ModelAdmin):
    
    inlines = [OrderItemInline]
    list_display = ('id', 'customer', 'status', 'amount_pay', 'created_at')  # Add a custom method for total amount
    list_display_links = ('id', 'customer', 'amount_pay')
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'customer__username')  # Search by order ID and customer username


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem) 