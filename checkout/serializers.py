from rest_framework import serializers
from .models import CartItem
from product.models import Product, Category


class ProductCategoryCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class ProductCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'short_text', 'product_photo', 'unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductCartSerializer(read_only=True)
    category = ProductCategoryCartSerializer(read_only=True)
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'category']


class CartItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('__all__')

