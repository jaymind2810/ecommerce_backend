from rest_framework import serializers
from .models import Product, Category, ProductImages


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('__all__')
    
    # def create(self, validated_data):
    #     print(validated_data, "-------In Serializer Create function ------------")
    #     return Product.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     # instance.first_name = validated_data.get('first_name', instance.first_name)
    #     instance.save()

    #     return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'  # Include all fields for Category


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImages
        fields = ('__all__')


class ProductAlldataSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'name' ,'short_text', 'description', 'unit_price', 'product_photo', 'category_id',
                    'manufacturer_name', 'manufacturer_brand', 'product_stock', 'cost_price', 'publish_status', 'visibility',
                    'last_published_date_time', 'create_by', 'create_date', 'last_modified', 'product_images')
