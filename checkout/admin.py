from django.contrib import admin
from .models import Cart, CartItem
from django.contrib.auth.models import Permission


class CartAdmin(admin.ModelAdmin):

    list_display = ('id','user', 'created_at', 'updated_at')
    list_display_links = ('id',)
    # list_editable = ('is_featured',)
    # search_fields = ('id', 'name', 'description', 'create_date')
    # list_filter = ('create_date',)

class CartItemAdmin(admin.ModelAdmin):

    list_display = ('id', 'cart','product', 'quantity', 'created_at', 'updated_at')
    list_display_links = ('id',)


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)