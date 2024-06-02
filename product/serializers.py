from rest_framework import serializers
from .models import Product, Category


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('__all__')
    
    def create(self, validated_data):
        print(validated_data, "-------In Serializer Create function ------------")
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.save()

        return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'  # Include all fields for Category

