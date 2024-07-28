from rest_framework import serializers
from .models import Payment



class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


# class OrderItemsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItems
#         fields = '__all__'


class AllPaymentItemsSerializer(serializers.ModelSerializer):
    # order_items = OrderItemsSerializer(many=True)
    class Meta:
        model = Payment
        fields = ['user', 'payment_refrence_id', 'status', 'amount', 'currency']