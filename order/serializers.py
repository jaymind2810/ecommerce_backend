from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('__all__')
    
    def create(self, validated_data):
        print(validated_data, "-------In Serializer Create function ------------")
        return Order.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.save()

        return instance


