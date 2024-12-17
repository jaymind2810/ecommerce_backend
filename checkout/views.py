from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import stripe
stripe.api_key = 'sk_test_51POKT1P2KIYLyQddL4wKfALiHpfAppLjcH8xYn6UUHAUnPREjtDFLsTwNLjdMV0ygqNoc65w4QhtsPpnUbUA3foq00yifkKMYf'

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated 
from .utils import (
    getAllCartItems,
    getCartItemDetail,
    createCartItem,
    updateCartItem,
    deleteCartItem,
    getAllAddresss,
    getAddressDetail,
    createAddress,
    updateAddress,
    deleteAddress,
)


class CartItemListAPIView(APIView):
    """
    API endpoint for listing and creating CartItems.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Retrieves a list of all CartItems.
        """
        try:
            response = getAllCartItems(request)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)

    def post(self, request, format=None):
        """
        Creates a new CartItem.
        """
        try:
            response = createCartItem(request)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)


class CartItemDetailAPIView(APIView):
    # permission_classes = (IsAuthenticated,)
    def get(self, request, pk, format=None):
        try:
            response = getCartItemDetail(request, pk)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, pk, format=None):
        try:
            response = updateCartItem(request, pk)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk, format=None):
        try:
            response = deleteCartItem(request, pk)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)


class AddressListAPIView(APIView):
    """
    API endpoint for listing and creating Addresss.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Retrieves a list of all Addresss.
        """
        try:
            response = getAllAddresss(request)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)

    def post(self, request, format=None):
        """
        Creates a new Address.
        """
        try:
            response = createAddress(request)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)


class AddressDetailAPIView(APIView):
    # permission_classes = (IsAuthenticated,)
    def get(self, request, pk, format=None):
        try:
            response = getAddressDetail(request, pk)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, pk, format=None):
        try:
            response = updateAddress(request, pk)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk, format=None):
        try:
            response = deleteAddress(request, pk)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def create_payment(request):
    try:
        data = request.data
        print(data, "-------data---")
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount="1000",
            currency='usd',
            # In the latest version of the API, specifying the `automatic_payment_methods` parameter is optional because Stripe enables its functionality by default.
            automatic_payment_methods={
                'enabled': True,
            },
        )
        return Response({
            'clientSecret': intent['client_secret']
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)

