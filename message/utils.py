from decimal import Decimal
from account.models import User
from .serializers import MessageSerializer
from .models import Message
from django.db.models import Q


def getAllMessages(request):
    try:
        print(request.GET, "--request data------")
        sender = request.GET.get('sender')
        reciever = request.GET.get('reciever')
        print(sender, reciever, "------sender -----reciever-------")
        messages = Message.objects.filter((Q(sender=sender), Q(reciever=reciever)) | (Q(sender=reciever), Q(reciever=sender))).order_by('-created_at')

        print(messages, "------messages========")

        # paginator = Paginator(messages, 10)  # Show 10 messages per page
        # page_number = request.GET.get('page')  # Get the page number from the request
        # page_obj = paginator.get_page(page_number)

        
        # messages = Message.objects.filter(sender=user_id) | Message.objects.filter(receiver=user_id)
        serializer = MessageSerializer(messages, many=True)
        return {
            "data": serializer.data,
            "status": 200,
            "message": "All Messages",
            "success": True,
        }
    except Exception as e:
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