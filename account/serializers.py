from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
)
from django.conf import settings
from six import text_type
from datetime import timedelta
import django.core.exceptions as exceptions

REMEMBER_ME_EXPIRY_TIME = timedelta(days=30)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """

    class Meta:
        model = User
        fields = ('__all__')
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        instance.save()
        return instance


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        try:
            data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
            token = self.get_token(self.user)
            # if self._kwargs["data"]["rememberMe"]:
            #     new_token = token.access_token
            #     new_token.set_exp(lifetime=REMEMBER_ME_EXPIRY_TIME)
            #     data["access"] = text_type(new_token)
            # else:
            #     data["access"] = text_type(token.access_token)
            new_token = token.access_token
            new_token.set_exp(lifetime=REMEMBER_ME_EXPIRY_TIME)
            data["access"] = text_type(new_token)
            
            data["userId"] = self.user.id
            data["user"] = self.user.email
            # data["is_baned"] = self.user.is_baned
            # data["bane_type"] = self.user.bane_type
            # return data
            return {
                "data": data,
                "status": 200,
                "message": "Login Successfully..!!",
                "success": True,
            }
        
        except Exception as e:
            return {
                "data": {},
                "status": 500,
                "message": "Somthing went wrong",
                "success": False,
            }


class RegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = User.objects.create_user(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            username=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class allUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email')