from rest_framework.authtoken.models import Token 
from order.serializers import NewOrderSerializer
from order.models import Order
from product.models import Product
from product.serializers import ProductSerializer
from .models import User
from checkout.models import Address, CartItem
from .serializers import (
    RegisterSerializer,
    UserSerializer,
)
from checkout.serializers import AddressSerializer, CartItemSerializer
from django.contrib.auth import authenticate, login


def getUserAllData(pk):
    try:
        user = User.objects.get(id=pk)
        userData = UserSerializer(user)
        address_datas = Address.objects.filter(user_id=pk)
        addressData = AddressSerializer(address_datas, many=True)
        user = User.objects.get(id=pk)
        carts = CartItem.objects.filter(user=pk)
        cart_items = CartItemSerializer(carts, many=True)

        orders_datas = Order.objects.filter(customer=pk)
        user_orders = NewOrderSerializer(orders_datas, many=True)

        all_user_data = {
            'user' : userData.data,
            'address_details' : addressData.data,
            'cart_items' : cart_items.data,
            'user_orders' : user_orders.data,
        }

        return {
            "data": all_user_data,
            "status": 200,
            "message": "All user Data",
            "success": True,
        }
    
    except Exception as e:
        return {
            "data": {},
            "status": 500,
            "message": "Somthing went wrong",
            "success": False,
        }


def getAllHomePageData(request):
    try:
        all_home_page_data = {}
        # Trending Products
        trending_products = Product.objects.filter(visibility='Public', publish_status='Published').order_by("?")[:4]
        productserializer = ProductSerializer(trending_products, many=True)
        all_home_page_data["trending_products"] = productserializer.data

        return {
            "data": all_home_page_data,
            "status": 200,
            "message": "All Home page Data",
            "success": True,
        }
    
    except Exception as e:
        return {
            "data": {},
            "status": 500,
            "message": "Somthing went wrong",
            "success": False,
        }
    

def validateUserLoginData(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return {
                "data": {},
                "status": 400,
                "message": "Username or Password are required.",
                "success": False,
            }

        user = authenticate(username=username, password=password)
        if not user:
            return {
                "data": {},
                "status": 401,
                "message": "Invalid credentials.",
                "success": False,
            }

        login(request, user)  # Log in the user
        token, _ = Token.objects.get_or_create(user=user)  # Generate a token (if using token-based auth)
        data = {'token': token.key}
        return {
            "data": data,
            "status": 200,
            "message": "Login Successfully..!!",
            "success": True,
        }
    
    except Exception as e:
        return {
            "data": {},
            "status": 500,
            "message": "Somthing went wrong",
            "success": False,
        }
    

def registerUser(request):
    try:
        data = request.data
        del data["password2"]
        email = data['email']
        data['username'] = email
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return {
                "data": serializer.data,
                "status": 200,
                "message": "Register Successfully..!!",
                "success": True,
            }
        return {
            "data": serializer.errors,
            "status": 400,
            "message": "Somthing went wrong",
            "success": False,
        }
    except Exception as e:
        return {
            "data": {},
            "status": 500,
            "message": "Somthing went wrong",
            "success": False,
        }
    
