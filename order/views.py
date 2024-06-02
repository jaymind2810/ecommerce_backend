from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderSerializer  # Import your order serializer
from .models import Order  # Import your Order model

class OrderListAPIView(APIView):

    def get(self, request, format=None):
        """
        Retrieves a list of all orders.
        """
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response({"status": "success", "data": serializer.data}, status=200)

    def post(self, request, format=None):
        """
        Creates a new order.
        """
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetailAPIView(APIView):
    """
    API endpoint for retrieving, updating, and deleting an individual order.
    """

    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return None

    def get(self, request, pk, format=None):
        order = self.get_object(pk)
        if not order:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order)
        return Response({"status": "success", "data": serializer.data}, status=200)
    
    def put(self, request, pk, format=None):
        order = self.get_object(pk)
        if not order:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        order = self.get_object(pk)
        if not order:
            return Response(status=status.HTTP_404_NOT_FOUND)
        order.delete()
        # return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"status": "success", "data": "Order Record Deleted"}, status=200)