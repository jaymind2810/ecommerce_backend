from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import stripe
from django.conf import settings

stripe.api_key = 'sk_test_51POKT1P2KIYLyQddL4wKfALiHpfAppLjcH8xYn6UUHAUnPREjtDFLsTwNLjdMV0ygqNoc65w4QhtsPpnUbUA3foq00yifkKMYf'

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CartItem, Address
from account.models import User
from .serializers import CartItemSerializer, CartItemsSerializer, AddressSerializer



class CartItemListCreateAPIView(APIView):
    def get(self, request):
        cart_items = CartItem.objects.all()
        serializer = CartItemSerializer(cart_items, many=True)
        return Response({"status": "success", "data": serializer.data}, status=200)

    def post(self, request):
        serializer = CartItemsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartItemDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            user = User.objects.get(id=pk)
            cart = CartItem.objects.filter(user=user.id)
            return cart
        except CartItem.DoesNotExist:
            return None

    def get(self, request, pk):
        cart_items = self.get_object(pk)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response({"status": "success", "data": serializer.data}, status=200)

    def put(self, request, pk):
        cart_item = CartItem.objects.get(id=request.data['id'])
        serializer = CartItemSerializer(cart_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        cart_item = CartItem.objects.get(id=request.data['id'])
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddressListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        addresses = Address.objects.all()
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressDetailAPIView(APIView):
    def get_object(self, pk):
        user = User.objects.get(id=pk)
        address = Address.objects.filter(user=user.id)
        return address
        
    def get(self, request, pk, *args, **kwargs):
        address = self.get_object(pk)
        serializer = AddressSerializer(address, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        address = self.get_object(pk)
        serializer = AddressSerializer(address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        address = self.get_object(pk)
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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

