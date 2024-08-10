from .models import User
from checkout.models import Address, CartItem
from .serializers import (
    UserSerializer,
)
from checkout.serializers import AddressSerializer, CartItemSerializer


def getUserAllData(pk):
    user = User.objects.get(id=pk)
    userData = UserSerializer(user)
    address_datas = Address.objects.filter(user_id=pk)
    addressData = AddressSerializer(address_datas, many=True)
    user = User.objects.get(id=pk)
    carts = CartItem.objects.filter(user=pk)
    cart_items = CartItemSerializer(carts, many=True)

    all_user_data = {
        'user' : userData.data,
        'address_details' : addressData.data,
        'cart_items' : cart_items.data,
    }

    return all_user_data

