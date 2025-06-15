from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser 
from .utils import (
    getAdminAllOrders,
    getAllOrders,
    getOrderDetail,
    createOrder,
    updateOrder,
    deleteOrder,
)

    
class OrderListAPIView(APIView):
    """
    API endpoint for listing and creating Orders.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Retrieves a list of all Orders.
        """
        try:
            response = getAllOrders(request)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)

    def post(self, request, format=None):
        """
        Creates a new Order.
        """
        try:
            response = createOrder(request)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)


class OrderDetailAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, pk, format=None):
        try:
            response = getOrderDetail(request, pk)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, pk, format=None):
        try:
            response = updateOrder(request, pk)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk, format=None):
        try:
            response = deleteOrder(request, pk)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        

class AdminOrderListAPIView(APIView):
    """
    API endpoint for listing and creating Orders.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        """
        Retrieves a list of all Orders.
        """
        try:
            response = getAdminAllOrders(request)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)

    def post(self, request, format=None):
        """
        Creates a new Order.
        """
        try:
            response = createOrder(request)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)