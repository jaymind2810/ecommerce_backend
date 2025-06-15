from decimal import Decimal
from account.models import User
from .serializers import MessageSerializer, MessageUserSerializer
from .models import Message
from django.db.models import Q


def getAllMessages(request):
    try:
        sender = request.GET.get('sender')
        receiver = request.GET.get('receiver')
        page = int(request.GET.get('page'))
        page_size = int(request.GET.get('page_size'))

        offset = (page - 1) * page_size
        message_data_dict = {}

        if not sender or not receiver:
            return {
                "data": {},
                "status": 400,
                "message": "Both sender and receiver IDs are required.",
                "success": False,
            }

        messages = Message.objects.filter(
            Q(sender_id=sender, receiver_id=receiver) |
            Q(sender_id=receiver, receiver_id=sender)
        ).order_by('-created_at')[offset:offset+page_size]

        messagesserializer = MessageSerializer(instance=messages, many=True)

        receiver_user = User.objects.get(pk=receiver)
        receiverUser = MessageUserSerializer(instance=receiver_user)
        sender_user = User.objects.get(pk=sender)
        senderUser = MessageUserSerializer(instance=sender_user)

        message_data_dict['messages'] = messagesserializer.data[::-1]
        message_data_dict['has_more'] = len(messages) == page_size
        message_data_dict['receiver_user'] = receiverUser.data
        message_data_dict['sender_user'] = senderUser.data

        return {
            "data": message_data_dict,
            "status": 200,
            "message": "All Messages",
            "success": True,
        }

    except Exception as e:
        print("Error:", e)
        return {
            "data": {},
            "status": 500,
            "message": "Something went wrong",
            "success": False,
        }
def createMessage(request):
    try:
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=request.user)
            return {
                "data": serializer.data,
                "status": 201,
                "message": "Message created successfully",
                "success": True,
            }
        return {
            "data": {},
            "status": 400,
            "message": "Invalid data",
            "success": False,
        }
    except Exception as e:
        return {
            "data": {},
            "status": 500,
            "message": "Something went wrong",
            "success": False,
        }

def getMessageDetail(request, pk):
    try:
        message = Message.objects.get(pk=pk)
        serializer = MessageSerializer(message)
        return {
            "data": serializer.data,
            "status": 200,
            "message": "Message details retrieved",
            "success": True,
        }
    except Message.DoesNotExist:
        return {
            "data": {},
            "status": 404,
            "message": "Message not found",
            "success": False,
        }

def updateMessage(request, pk):
    try:
        message = Message.objects.get(pk=pk)
        serializer = MessageSerializer(message, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return {
                "data": serializer.data,
                "status": 200,
                "message": "Message updated successfully",
                "success": True,
            }
        return {
            "data": {},
            "status": 400,
            "message": "Invalid data",
            "success": False,
        }
    except Message.DoesNotExist:
        return {
            "data": {},
            "status": 404,
            "message": "Message not found",
            "success": False,
        }
    except Exception as e:
        return {
            "data": {},
            "status": 500,
            "message": "Something went wrong",
            "success": False,
        }

def deleteMessage(request, pk):
    try:
        message = Message.objects.get(pk=pk)
        message.delete()
        return {
            "data": {},
            "status": 200,
            "message": "Message deleted successfully",
            "success": True,
        }
    except Message.DoesNotExist:
        return {
            "data": {},
            "status": 404,
            "message": "Message not found",
            "success": False,
        }
    except Exception as e:
        return {
            "data": {},
            "status": 500,
            "message": "Something went wrong",
            "success": False,
        }