from account.models import User
from order.serializers import NewOrderSerializer, OrderSerializer
from order.models import Order, OrderItem
from checkout.models import CartItem


def getAllOrders(request):
    try:
        Orders = Order.objects.all()
        serializer = OrderSerializer(Orders, many=True)
        return {
            "data": serializer.data,
            "status": 200,
            "message": "All Orders",
            "success": True,
        }
    
    except Exception as e:
        return {
            "data": {},
            "status": 500,
            "message": "Somthing went wrong",
            "success": False,
        }
    
def createOrder(request):
    try: 
        # Extract and prepare order data from the request
        cart_items = request.data.get('order_items', [])
        print(cart_items, "---- Cart Items ------------")
        customer = request.data.get('user')
        address = request.data.get('address', {})
        amount = request.data.get('amount')
        payment_method = request.data.get('payment_method')

        # Construct the order data
        order_data = {
            "customer": customer,
            "status": "confirm",
            "address": address.get("id"),
            "amount_pay": float(amount) if amount else 0.0,
            "payment_method": payment_method,
            "payment_confirmed": True,
            "items": [
                {
                    "product": item.get("product", {}).get("id"),
                    "quantity": item.get("quantity"),
                    "unit_price": float(item.get("product", {}).get("unit_price", 0.0))
                }
                for item in cart_items
            ]
        }


        # Serialize the order data
        serializer = OrderSerializer(data=order_data)

        # Validate and save the order
        if serializer.is_valid():
            order = serializer.save()

            cart_item_ids = [item.get("id") for item in cart_items]
            if len(cart_item_ids) >= 1:
                cart_items = CartItem.objects.filter(id__in=cart_item_ids)
                cart_items.delete()

            new_serializer = NewOrderSerializer(order)
            return {
                "data": new_serializer.data,
                "status": 200,
                "message": "Order Created Successfully.",
                "success": True,
            }            
        else:
            return {
                    "data": serializer.errors,
                    "status": 400,
                    "message": "Validation failed.",
                    "success": False,
                }
    except Exception as e:
        return {
            "data": {},
            "status": 500,
            "message": "Somthing went wrong",
            "success": False,
        }

def getOrderDetail(request, pk):
    try: 
        Order_data = Order.objects.get(id=pk)
       
        if Order_data:
            serializer = NewOrderSerializer(Order_data)
            return {
                "data": serializer.data,
                "status": 200,
                "message": "Order Fatch Successfully.",
                "success": True,
            }
        else :
            return {
                "data": {},
                "status": 400,
                "message": "Order not found.",
                "success": False,
            }
    except Exception as e:
        return {
            "data": {},
            "status": 500,
            "message": "Somthing went wrong",
            "success": False,
        }

def updateOrder(request, pk):
    try: 
        Order = Order.objects.get(pk=pk)
        if Order:
            serializer = OrderSerializer(Order, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return {
                    "data": serializer.data,
                    "status": 200,
                    "message": "Order Updated Successfully.",
                    "success": True,
                }
            else:
                return {
                    "data": serializer.errors,
                    "status": 400,
                    "message": "Something went wrong..!!",
                    "success": True,
                }
        else:
            return {
                "data": {},
                "status": 400,
                "message": "Order not found.",
                "success": True,
            }
    except Exception as e:
        return {
            "data": {},
            "status": 500,
            "message": "Somthing went wrong",
            "success": False,
        }

def deleteOrder(request, pk):
    try: 
        Order = Order.objects.get(pk=pk)
        if Order:
            Order.delete()
            return {
                "data": {},
                "status": 200,
                "message": "Order Deleted Successfully.",
                "success": True,
            }
        else:
            return {
                "data": {},
                "status": 400,
                "message": "Order not found.",
                "success": True,
            }
    except Exception as e:
        return {
            "data": {},
            "status": 500,
            "message": "Somthing went wrong",
            "success": False,
        }