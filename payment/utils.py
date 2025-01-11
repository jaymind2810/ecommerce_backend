from checkout.models import Address, CartItem
from checkout.serializers import AddressSerializer, CartItemSerializer, CartItemsSerializer
from account.models import User
import stripe
import os
from account.serializers import UserSerializer

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