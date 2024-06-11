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

    # def create(self, validated_data):
        # user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        # user.save()
        # return user

    def update(self, instance, validated_data):
        # instance.username = validated_data.get('username', instance.username)
        # instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        print(attrs, "======attrs------------")
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        print(data, "========data=========")
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
        return data


class RegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        print(validated_data, "=====+Validate Data========")
        user = User.objects.create_user(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            username=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
