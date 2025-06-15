from decimal import Decimal
from math import ceil
from account.models import User
from payment.serializers import PaymentSerializer
from payment.models import Payment
from order.serializers import AdminOrderSerializer, NewOrderSerializer, OrderSerializer
from order.models import Order, OrderItem
from checkout.models import CartItem
from django.db.models import Q


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
        res_data = {}
        cart_items = request.data.get('order_items', [])
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
            "payment_confirmed": False,
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
            
            user = User.objects.get(id=customer)

            # Create Payment record ..
            payment_record_data = {
                'amount': Decimal(str(amount)),
                'user': user,
                'status': "pending",
                'currency': "usd",
                'payment_method': 'cod',
                'is_promocode_used': False,
                # 'transaction_id': data.get('payment_refrence_id'),
                # 'customer_id': data.get('customer_id'),
                'order': order,
                # 'payment_method_id': data.get('payment_method_id'),
            }

            payment_record = Payment(**payment_record_data)
            payment_record.save()

            payment_serializer = PaymentSerializer(payment_record)
            res_data['payment'] = payment_serializer.data

            new_serializer = NewOrderSerializer(order)
            res_data['order'] = new_serializer.data

            cart_item_ids = [item.get("id") for item in cart_items]
            if len(cart_item_ids) >= 1:
                cart_items = CartItem.objects.filter(id__in=cart_item_ids)
                cart_items.delete()

            return {
                "data": res_data,
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
    

def getAdminAllOrders(request):
    try:
        # Sorting
        order = request.GET.get('sort', 'created_at')

        # Filtering by categories
        orders = Order.objects.all().order_by(order)
        # Search query
        search_query = request.GET.get('q', '')
        if search_query:
            orders = orders.filter(
                # Q(name__icontains=search_query) | Q(description__icontains=search_query)
                Q(customer__first_name__in=search_query) | Q(customer__last_name__in=search_query)
            )

        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        total_count = orders.count()

        start = (page - 1) * page_size
        end = start + page_size

        paginated_orders = orders[start:end]

        serializer = AdminOrderSerializer(paginated_orders, many=True)

        # Determine if there's more data
        has_more = end < total_count

        return {
            "data": serializer.data,
            "status": 200,
            "message": "All Orders",
            "success": True,
            "pagination": {
                "current_page": page,
                "page_size": page_size,
                "total_count": total_count,
                "total_pages": ceil(total_count / page_size),
                "has_more": has_more,
            },
        }

    except Exception as e:
        return {
            "data": {},
            "status": 500,
            "message": "Somthing went wrong",
            "success": False,
        }
    