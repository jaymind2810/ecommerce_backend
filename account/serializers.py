from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """

    class Meta:
        model = User
        fields = ('__all__')
        extra_kwargs = {'password': {'write_only': True}}

    # def create(self, validated_data):
        # user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        # user.save()
        # return user

    def update(self, instance, validated_data):
        # instance.username = validated_data.get('username', instance.username)
        # instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance

