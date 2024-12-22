from checkout.models import Address, CartItem
from checkout.serializers import AddressSerializer, CartItemSerializer, CartItemsSerializer
from account.models import User


def getAllCartItems(request):
    try:
        cart_items = CartItem.objects.all()
        serializer = CartItemSerializer(cart_items, many=True)
        return {
            "data": serializer.data,
            "status": 200,
            "message": "All CartItems",
            "success": True,
        }
    
    except Exception as e:
        return {
            "data": {},
            "status": 500,
            "message": "Somthing went wrong",
            "success": False,
        }
    
def createCartItem(request):
    try: 
        serializer = CartItemsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return {
                "data": serializer.data,
                "status": 200,
                "message": "CartItem Created Successfully.",
                "success": True,
            }
        else:
            return {
                "data": serializer.errors,
                "status": 404,
                "message": "Something went wrong..!!",
                "success": False,
            }
    except Exception as e:
        return {
            "data": {},
            "status": 500,
            "message": "Somthing went wrong",
            "success": False,
        }
    
def getCartItemDetail(request, pk):
    try: 
        user = User.objects.get(id=pk)
        cart_items = CartItem.objects.filter(user=user.id)
        if cart_items:
            serializer = CartItemSerializer(cart_items, many=True)
            return {
                "data": serializer.data,
                "status": 200,
                "message": "CartItem Created Successfully.",
                "success": True,
            }
        else :
            return {
                "data": {},
                "status": 404,
                "message": "CartItem not found.",
                "success": False,
            }
    except Exception as e:
        return {
            "data": {},
            "status": 500,
            "message": "Somthing went wrong",
            "success": False,
        }

def updateCartItem(request, pk):
    try: 
        cart_item = CartItem.objects.get(id=request.data['id'])
        if cart_item:
            serializer = CartItemSerializer(cart_item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return {
                    "data": serializer.data,
                    "status": 200,
                    "message": "CartItem Updated Successfully.",
                    "success": True,
                }
            else:
                return {
                    "data": serializer.errors,
                    "status": 404,
                    "message": "Something went wrong..!!",
                    "success": False,
                }
        else:
            return {
                "data": {},
                "status": 404,
                "message": "CartItem not found.",
                "success": False,
            }
    except Exception as e:
        return {
            "data": {},
            "status": 500,
            "message": "Somthing went wrong",
            "success": False,
        }

def deleteCartItem(request, pk):
    try:
        cart_item = CartItem.objects.get(id=request.data['id']) 
        # CartItem = CartItem.objects.get(id=request.GET('id')) 
        if cart_item:
            cart_item.delete()
            return {
                "data": {},
                "status": 200,
                "message": "CartItem Deleted Successfully.",
                "success": True,
            }
        else:
            return {
                "data": {},
                "status": 404,
                "message": "CartItem not found.",
                "success": False,
            }
    except Exception as e:
        return {
            "data": {},
            "status": 500,
            "message": "Somthing went wrong",
            "success": False,
        }

# ================================  Address =========================================
def getAllAddresss(request):
    try:
        address = Address.objects.all()
        serializer = AddressSerializer(address, many=True)
        return {
            "data": serializer.data,
            "status": 200,
            "message": "All Addresss",
            "success": True,
        }
    
    except Exception as e:
        return {
            "data": {},
            "status": 500,
            "message": "Somthing went wrong",
            "success": False,
        }
    
def createAddress(request):
    try: 
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return {
                "data": serializer.data,
                "status": 200,
                "message": "Address Created Successfully.",
                "success": True,
            }
        else:
            return {
                "data": serializer.errors,
                "status": 404,
                "message": "Something went wrong..!!",
                "success": False,
            }
    except Exception as e:
        return {
            "data": {},
            "status": 500,
            "message": "Somthing went wrong",
            "success": False,
        }
    
def getAddressDetail(request, pk):
    try: 
        user = User.objects.get(id=pk)
        address = Address.objects.filter(user=user.id)
        if address:
            serializer = AddressSerializer(address, many=True)
            return {
                "data": serializer.data,
                "status": 200,
                "message": "Address Created Successfully.",
                "success": True,
            }
        else :
            return {
                "data": {},
                "status": 404,
                "message": "Address not found.",
                "success": False,
            }
    except Exception as e:
        return {
            "data": {},
            "status": 500,
            "message": "Somthing went wrong",
            "success": False,
        }

def updateAddress(request, pk):
    try: 
        user = User.objects.get(id=pk)
        address = Address.objects.filter(user=user.id)
        if address:
            serializer = AddressSerializer(address, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return {
                    "data": serializer.data,
                    "status": 200,
                    "message": "Address Updated Successfully.",
                    "success": True,
                }
            else:
                return {
                    "data": serializer.errors,
                    "status": 404,
                    "message": "Something went wrong..!!",
                    "success": False,
                }
        else:
            return {
                "data": {},
                "status": 404,
                "message": "Address not found.",
                "success": False,
            }
    except Exception as e:
        return {
            "data": {},
            "status": 500,
            "message": "Somthing went wrong",
            "success": False,
        }

def deleteAddress(request, pk):
    try: 
        address = Address.objects.get(id=pk)
        if address:
            address.delete()
            return {
                "data": {},
                "status": 204,
                "message": "Address Deleted Successfully.",
                "success": True,
            }
        else:
            return {
                "data": {},
                "status": 404,
                "message": "Address not found.",
                "success": False,
            }
    except Exception as e:
        return {
            "data": {},
            "status": 500,
            "message": "Somthing went wrong",
            "success": False,
        }
