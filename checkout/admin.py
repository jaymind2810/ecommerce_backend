from django.contrib import admin
from .models import CartItem
from django.contrib.auth.models import Permission


class CartItemAdmin(admin.ModelAdmin):

    list_display = ('id', 'product', 'quantity')
    list_display_links = ('id',)


admin.site.register(CartItem, CartItemAdmin)