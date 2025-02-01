from rest_framework import serializers

from checkout.serializers import AddressSerializer
from product.models import Product
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'unit_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "customer", "status", "address", "payment_method", "payment_confirmed", "amount_pay", "items"]

    def create(self, validated_data):
        # Extract and remove the nested `items` data
        items_data = validated_data.pop('items')

        # Create the `Order` instance
        order = Order.objects.create(**validated_data)

        # Create `OrderItem` instances for the order
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order


class ProductOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'short_text', 'product_photo', 'unit_price']


class NewOrderItemSerializer(serializers.ModelSerializer):
    product = ProductOrderSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'unit_price']


class NewOrderSerializer(serializers.ModelSerializer):
    items = NewOrderItemSerializer(many=True, source='order_items')
    address = AddressSerializer()

    class Meta:
        model = Order
        fields = ["id", "customer", "status", "address", "payment_method", "payment_confirmed", "amount_pay", "updated_at", "created_at", "items"]
