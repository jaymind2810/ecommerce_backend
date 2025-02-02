from django.contrib import admin
from .models import Payment
from checkout.admin import CartItemAdmin


class PaymentAdmin(admin.ModelAdmin):
    
    list_display = ('id' ,'user', 'payment_method',  'status', 'amount', 'created_at')  # Add a custom method for total amount
    list_display_links = ('id', 'user', 'payment_method')
    list_filter = ('status','payment_method',)
    search_fields = ('user__username',)

    fieldsets = [
        ('Payment info', {
            'fields': ['user', 'order', 'amount', "status", 'payment_method']
        }),
        ('Other Details', {
            'fields': ['transaction_id', 'payment_method_id', 'currency','is_promocode_used', 'promocode_amount'],
            'classes': ['wide',],
            'description': 'Payment details of the model.',
        }),
    ]


admin.site.register(Payment, PaymentAdmin)