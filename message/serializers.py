from rest_framework import serializers
from .models import Message
from account.models import User



class MessageUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'user_photo']


class MessageSerializer(serializers.ModelSerializer):
    sender = MessageUserSerializer(read_only=True)
    receiver = MessageUserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_text', 'is_popup', 'is_read', 'is_deleted_from_sender', 'is_deleted_from_receiver', 'is_delete', 'created_at', 'sender', 'receiver']  


# class MessageSerializer(serializers.ModelSerializer):
#     user = MessageUserSerializer(read_only=True)

#     class Meta:
#         model = Message
#         fields = '__all__'  