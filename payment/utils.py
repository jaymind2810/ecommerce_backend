from decimal import Decimal

from django.shortcuts import get_object_or_404
from checkout.models import Address, CartItem
from checkout.serializers import AddressSerializer, CartItemSerializer, CartItemsSerializer
from account.models import User
import stripe
import os
from account.serializers import UserSerializer
from payment.serializers import PaymentSerializer
from order.models import Order
from order.serializers import NewOrderSerializer, OrderSerializer
from payment.models import Payment

# stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
stripe.api_key = "sk_test_51POKT1P2KIYLyQddL4wKfALiHpfAppLjcH8xYn6UUHAUnPREjtDFLsTwNLjdMV0ygqNoc65w4QhtsPpnUbUA3foq00yifkKMYf"


def createStripeCustomer(request):
    try: 
        data = request.data
        if 'user_id' in data:
            user = User.objects.get(id=data['user_id'])
            if user.user_stripe_id:
                if 'paymentMethod' in data:
                    # Retrieve existing payment methods
                    existing_cards = stripe.PaymentMethod.list(
                        customer=user.user_stripe_id,
                        type="card",
                    )


                    card_fingerprint = stripe.PaymentMethod.retrieve(data['paymentMethod']['id'])

                    # Compare fingerprints
                    for card in existing_cards.data:
                        if card.card.fingerprint == card_fingerprint.card.fingerprint:
                            return {
                                "data": { 'customer_id' : user.user_stripe_id},
                                "status": 200,
                                "message": "Card is already added.",
                                "success": True,
                            }
                        
                    new_paymnet_method = stripe.PaymentMethod.attach(data['paymentMethod']['id'],
                            customer=user.user_stripe_id,
                        )
                    return {
                        "data": new_paymnet_method,
                        "status": 200,
                        "message": "Payment Method Added to User",
                        "success": True,
                    }
                else:
                    return {
                        "data": {},
                        "status": 500,
                        "message": "Somthing went wrong. Payment Method not defined.",
                        "success": False,
                    }
            else:
                name = user.first_name
                email = user.email

                customers = stripe.Customer.list(
                    email=email,
                    limit=1
                )

                if customers:
                    user.user_stripe_id = customers['data'][0]['id']
                    user.save()
                    serializer = UserSerializer(user)

                    existing_cards = stripe.PaymentMethod.list(
                        customer=customers['data'][0]['id'],
                        type="card",
                    )
                    card_fingerprint = stripe.PaymentMethod.retrieve(data['paymentMethod']['id'])

                    # Compare fingerprints
                    for card in existing_cards.data:
                        if card.card.fingerprint == card_fingerprint.card.fingerprint:
                            return {
                                "data": serializer.data,
                                "status": 200,
                                "message": "User data retrived successfully",
                                "success": True,
                            }
                        
                    stripe.PaymentMethod.attach(data['paymentMethod']['id'],
                        customer=customers['data'][0]['id'],
                    )
                
                    return {
                        "data": serializer.data,
                        "status": 200,
                        "message": "User data retrived successfully",
                        "success": True,
                    }

                customer = stripe.Customer.create(
                    name=name,
                    email=email,
                )
                customer_id = customer['id']

                if 'paymentMethod' in data:
                    stripe.PaymentMethod.attach(data['paymentMethod']['id'],
                    customer=customer_id,
                )
                    
                user.user_stripe_id = customer_id
                user.save()
                serializer = UserSerializer(user)
            
                return {
                    "data": serializer.data,
                    "status": 200,
                    "message": "User data retrived successfully",
                    "success": True,
                }
        else:
            return {
                "data": {},
                "status": 500,
                "message": "Somthing went wrong. User not found",
                "success": False,
            }
        
    except Exception as e:
        return {
            "data": {},
            "status": 500,
            "message": "Somthing went wrong",
            "success": False,
        }
    
def retriveCustomerPaymentMethods(request):
    try: 
        data = request.data
        if 'user_stripe_id' in data:
            customer_id = data['user_stripe_id'] 
            payment_methods = stripe.Customer.list_payment_methods(
                customer_id,
                limit=3,
            )
            return {
                "data": payment_methods,
                "status": 200,
                "message": "Payment methods retrived successfully",
                "success": True,
            }
        else :
            return {
                "data": [],
                "status": 200,
                "message": "Customer id not found.",
                "success": False,
            }
        
    except Exception as e:
        return {
            "data": {},
            "status": 500,
            "message": "Somthing went wrong",
            "success": False,
        }
    
def deleteCustomerPaymentMethods(request):
    try: 
        data = request.data
        if 'user_stripe_id' in data:
            if 'card' in data:
                payment_method_id = data['card']['id'] 
                data = stripe.PaymentMethod.detach(payment_method_id)
                # customer_id = data['user_stripe_id']
                # card_id = data['card']['card']['fingerprint'] 
                # customer_id = data['card']['customer']
                # data = stripe.Customer.delete_source(
                #     customer=customer_id,
                #     source=card_id,
                # )            
                # payment_methods = stripe.Customer.list_payment_methods(
                #     customer_id,
                #     limit=3,
                # )
                return {
                    # "data": payment_methods,
                    "data": data,
                    "status": 200,
                    "message": "Card deleted",
                    "success": True,
                }
        else :
            return {
                "data": [],
                "status": 200,
                "message": "Customer id not found.",
                "success": False,
            }
        
    except Exception as e:
        return {
            "data": {},
            "status": 500,
            "message": "Somthing went wrong",
            "success": False,
        }
    
def createStripePaymentIntent(request):
    try: 
        data = request.data
        amount_total = data['amount']
        customer_id = None
        res_data = {}

        if 'user_id' in data:
            user = User.objects.get(id=data['user_id'])

        if 'customer_id' in data:
            customer_id = data['customer_id']

        if 'payment_method_id' in data:
            payment_method = data['payment_method_id']

        # ===== Order Record Create ===============
        cart_items = request.data.get('order_items', [])
        customer = request.data.get('user_id')
        address = request.data.get('address', {})
        amount = request.data.get('amount')

        # Construct the order data
        order_data = {
            "customer": customer,
            "status": "processing",
            "address": address.get("id"),
            "amount_pay": float(amount) if amount else 0.0,
            "payment_method": 'stripe',
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
            new_serializer = NewOrderSerializer(order)
            res_data['order'] = new_serializer.data
        

        intent = stripe.PaymentIntent.create( 
            amount=amount_total * 100,
            currency="usd",
            automatic_payment_methods={
                "enabled": True,
                "allow_redirects":"always"
            },
            customer= customer_id,
            payment_method=payment_method,
        )

        if intent:
            res_data['intent'] = intent

            return {
                "data": res_data,
                "status": 200,
                "message": "Payment Intent Created Successfully",
                "success": True,
            }
        else:
            return {
                "data": {},
                "status": 500,
                "message": "Somthing went wrong. User not found",
                "success": False,
            }
        
    except Exception as e:
        return {
            "data": {},
            "status": 500,
            "message": "Somthing went wrong",
            "success": False,
        }

def createStripePaymentRecord(request):
    try: 
        data = request.data
        print(data, "======Data-------------")

        cart_items_data = data.get('cart_items', [])
        res_data = {}

        amount_total = data.get('amount', 0)
        if 'user_id' in data:
            user = User.objects.get(id=data['user_id'])

        is_promocode_used=False
        # for item in cart_items_data:
        #     promo_code = item.get('promo_code')
        #     if promo_code is not None:
        #         is_promocode_used = True
        #         break

        order_data = data.get('order')
        if not order_data:
            return {
                "data": {},
                "status": 400,
                "message": "Invalid order data",
                "success": False,
            }
        
        order = get_object_or_404(Order, id=order_data['id'])
        if order_data:
            order.status = "confirm"
            order.payment_confirmed = True
            order.save()

            cart_item_ids = [item.get("id") for item in cart_items_data]
            if cart_item_ids:
                CartItem.objects.filter(id__in=cart_item_ids).delete()

            new_order_serializer = NewOrderSerializer(order)
            res_data['order'] = new_order_serializer.data
        
        payment_record_data = {
            'amount': Decimal(str(amount_total)),
            'user': user,
            'status': "done" if data.get('status') == "DONE" else "fail",
            'currency': "usd",
            'payment_method': 'stripe',
            'is_promocode_used': is_promocode_used,
            'transaction_id': data.get('payment_refrence_id'),
            'customer_id': data.get('customer_id'),
            'order': order,
            'payment_method_id': data.get('payment_method_id'),
        }

        payment_record = Payment(**payment_record_data)
        payment_record.save()

        print(payment_record, "--------_Payment Recordpppp")

        payment_serializer = PaymentSerializer(payment_record)
        res_data['payment'] = payment_serializer.data

        print(res_data, "====res_datares_datares_datares_data")

        if res_data:
            return {
                "data": res_data,
                "status": 200,
                "message": "Payment Successfully Done.",
                "success": True,
            }
        else:
            return {
                "data": {},
                "status": 500,
                "message": "Somthing went wrong. User not found",
                "success": False,
            }
        
    except Exception as e:
        return {
            "data": {},
            "status": 500,
            "message": "Somthing went wrong",
            "success": False,
        }
  