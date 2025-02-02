from rest_framework import serializers
from .models import Payment



class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'



class AllPaymentItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['user', 'transaction_id', 'status', 'amount', 'currency']