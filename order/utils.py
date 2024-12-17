from order.serializers import OrderSerializer
from order.models import Order


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
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return {
                "data": serializer.data,
                "status": 200,
                "message": "Order Created Successfully.",
                "success": True,
            }
        else:
            return {
                "data": serializer.errors,
                "status": 400,
                "message": "Something went wrong..!!",
                "success": True,
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
        Order = Order.objects.get(pk=pk)
        if Order:
            serializer = OrderSerializer(Order)
            return {
                "data": serializer.data,
                "status": 200,
                "message": "Order Created Successfully.",
                "success": True,
            }
        else :
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