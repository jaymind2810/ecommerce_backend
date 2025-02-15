from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated 
from .utils import (
    getAllMessages,
    createMessage,
    getMessageDetail,
    updateMessage,
    deleteMessage,
)


class MessageListAPIView(APIView):
    """
    API endpoint for listing and creating Messages.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Retrieves a list of all Messages.
        """
        try:
            response = getAllMessages(request)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)

    def post(self, request, format=None):
        """
        Creates a new Message.
        """
        try:
            response = createMessage(request)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)


class MessageDetailAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, format=None):
        try:
            response = getMessageDetail(request, pk)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, pk, format=None):
        try:
            response = updateMessage(request, pk)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk, format=None):
        try:
            response = deleteMessage(request, pk)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
