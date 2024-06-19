import stripe
import json
import os
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework import status

stripe.api_version = '2023-10-16'
stripe.api_key = settings.STRIPE_SECRET_KEY


@api_view(['GET'])
def get_config(request):
    return Response({'publishableKey': settings.STRIPE_PUBLISHABLE_KEY})

def calculate_tax(orderAmount, currency):
    tax_calculation = stripe.tax.Calculation.create(
        currency=currency,
        customer_details={
            "address": {
                "line1": "10709 Cleary Blvd",
                "city": "Plantation",
                "state": "FL",
                "postal_code": "33324",
                "country": "US",
            },
            "address_source": "shipping",
        },
        line_items=[
            {
                "amount": orderAmount,  # Amount in cents
                "reference": "ProductRef",
                "tax_behavior": "exclusive",
                "tax_code": "txcd_30011000"
            }
        ],
        shipping_cost={"amount": 300}
    )
    return tax_calculation

@api_view(['POST'])
def create_payment(request):
    data = request.data
    payment_method_type = data.get('paymentMethodType')
    currency = data.get('currency')
    orderAmount = 5999
    calcuateTax = False  # Set this as needed

    formatted_payment_method_type = ['link', 'card'] if payment_method_type == 'link' else [payment_method_type]
    if calcuateTax:
        taxCalculation = calculate_tax(orderAmount, currency)
        params = {
            'payment_method_types': formatted_payment_method_type,
            'amount': taxCalculation['amount_total'],
            'currency': currency,
            "metadata": {
                'tax_calculation': taxCalculation['id']
            }
        }
    else:
        params = {
            'payment_method_types': formatted_payment_method_type,
            'amount': orderAmount,
            'currency': currency
        }

    if payment_method_type == 'acss_debit':
        params['payment_method_options'] = {
            'acss_debit': {
                'mandate_options': {
                    'payment_schedule': 'sporadic',
                    'transaction_type': 'personal'
                }
            }
        }

    try:
        intent = stripe.PaymentIntent.create(**params)
        return Response({'clientSecret': intent.client_secret})
    except stripe.error.StripeError as e:
        return Response({'error': {'message': str(e)}}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': {'message': str(e)}}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_payment_next(request):
    payment_intent = request.GET.get("payment_intent")
    intent = stripe.PaymentIntent.retrieve(payment_intent)
    return redirect(f'/success?payment_intent_client_secret={intent.client_secret}')

@api_view(['GET'])
def get_success(request):
    return render(request, 'success.html')

@api_view(['POST'])
def webhook_received(request):
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    request_data = json.loads(request.body)

    if webhook_secret:
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.body, sig_header=signature, secret=webhook_secret)
            data = event['data']
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        event_type = event['type']
    else:
        data = request_data['data']
        event_type = request_data['type']
    data_object = data['object']

    if event_type == 'payment_intent.succeeded':
        print('💰 Payment received!')
    elif event_type == 'payment_intent.payment_failed':
        print('❌ Payment failed.')
    return Response({'status': 'success'})
