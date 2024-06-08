from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status  # Import for handling HTTP status codes
from .serializers import ProductSerializer  # Import your product serializer
from .models import Product  # Import your Product model

class ProductListAPIView(APIView):
    """
    API endpoint for listing and creating products.
    """

    def get(self, request):
        """
        Retrieves a list of all products.
        """

        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({"status": "success", "data": serializer.data}, status=200)

    def post(self, request, format=None):
        """
        Creates a new product.
        """
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailAPIView(APIView):
    """
    API endpoint for retrieving, updating, and deleting an individual product.
    """

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response({"status": "success", "data": serializer.data}, status=200)

    def put(self, request, pk, format=None):
        product = self.get_object(pk)
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product = self.get_object(pk)
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND)
        product.delete()
        # return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"status": "success", "data": "Product Record Deleted"}, status=200)