from django.contrib import admin
from .models import Payment
from checkout.admin import CartItemAdmin


class PaymentAdmin(admin.ModelAdmin):
    
    # inlines = [CartItemAdmin]
    list_display = ('user', 'transaction_id', 'payment_method',  'status', 'amount', 'is_promocode_used', 'created_at')  # Add a custom method for total amount
    list_filter = ('status','payment_method',)
    search_fields = ('user__username',) 


admin.site.register(Payment, PaymentAdmin)