from django.contrib import admin
from .models import CartItem, Address
from django.contrib.auth.models import Permission


class CartItemAdmin(admin.ModelAdmin):

    list_display = ('id', 'product', 'quantity', 'updated_at')
    list_display_links = ('id',)


class AddressAdmin(admin.ModelAdmin):

    list_display = ('id', 'user_id','country')
    list_display_links = ('id',)
    fieldsets = (
        ('User Contact Info', {'fields': ('user_id', 'phone_number', 'email')}),
        ('Address Info', {'fields': ('street', 'city', 'state', 'country', 'postal_code')}),
        ('Other Info', {'fields': ('is_delete',)}),
    )


admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Address, AddressAdmin)