from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status  # Import for handling HTTP status codes
from rest_framework.permissions import IsAuthenticated 
from .utils import (
    getAllProducts,
    getProductDetail,
    createProduct,
    updateProduct,
    deleteProduct,
    getAllTrendingProducts,
    getAllRelatedProducts,
)


class ProductListAPIView(APIView):
    """
    API endpoint for listing and creating products.
    """
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Retrieves a list of all products.
        """
        try:
            response = getAllProducts(request)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)

    def post(self, request, format=None):
        """
        Creates a new product.
        """
        try:
            response = createProduct(request)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)


class ProductDetailAPIView(APIView):
    # permission_classes = (IsAuthenticated,)
    def get(self, request, pk, format=None):
        try:
            response = getProductDetail(request, pk)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, pk, format=None):
        try:
            response = updateProduct(request, pk)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk, format=None):
        try:
            response = deleteProduct(request, pk)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
    

class TrendingProductListAPIView(APIView):
    # permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            response = getAllTrendingProducts(request)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
    

class RelatedProductListAPIView(APIView):
    # permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            response = getAllRelatedProducts(request)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
