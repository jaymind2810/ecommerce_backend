from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import stripe
from django.conf import settings
from account.models import User
from .models import Payment
from .serializers import PaymentSerializer
from .serializers import PaymentSerializer, AllPaymentItemsSerializer
from decimal import Decimal
import os
from .utils import (
    createStripeCustomer,
    retriveCustomerPaymentMethods,
    deleteCustomerPaymentMethods,
    createStripePaymentIntent,
    createStripePaymentRecord
)

@api_view(['POST'])
def create_stripe_customer(request):
    try:
        response = createStripeCustomer(request)
        return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def retrive_customer_paymentMethods(request):    
    try:
        response = retriveCustomerPaymentMethods(request)
        return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
    
@api_view(['DELETE'])
def delete_customer_paymentMethods(request):    
    try:
        response = deleteCustomerPaymentMethods(request)
        return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
    

@api_view(['POST'])
def create_stripe_payment_intent(request):
    try:
        response = createStripePaymentIntent(request)
        return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def create_stripe_payment_record(request):
    try:
        response = createStripePaymentRecord(request)
        return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)



@api_view(['POST'])
def create_paypal_payment(request):
    try:
        data = request.data

        amount_total = data['amount']
        if 'user_id' in data:
            user = User.objects.get(id=data['user_id'])

        is_promocode_used=False
        for item in data['order_items']:
            promo_code = item.get('promo_code')
            if promo_code is not None:
                is_promocode_used = True
                break

        payment_record_data = {
            'amount': Decimal(amount_total),
            'user': user,
            'status': "DONE",
            'currency':"usd",
            'payment_method': 'PayPal',
            'payment_refrence_id' : data['paypal_details']['purchase_units'][0]['payments']['captures'][0]['id'] if data['paypal_details']['purchase_units'][0]['payments']['captures'][0]['id'] else data['paypal_details']['id'],
            'is_promocode_used': is_promocode_used,
            'customer_id': data['paypal_details']['payer']['payer_id'],
        }

        payment_record_id = Payment(**payment_record_data)
        payment_record_id.save()
        payment_data = {
            'payment_id' : payment_record_id.id
        }
        return Response({"status": "success", "data": payment_data}, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
    


class AllPaymentItemListCreate(APIView):
    def get(self, request):
        payments = Payment.objects.all()
        serializer = AllPaymentItemsSerializer(payments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AllPaymentItemsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PaymentListCreate(APIView):
    def get(self, request):
        payments = Payment.objects.all()
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        payment_refrence_id = request.data['payment_refrence_id']
        payment_record_id = Payment.objects.filter(payment_refrence_id = payment_refrence_id)
        if payment_record_id:
            payment = Payment.objects.get(id=payment_record_id[0].id) 
            payment.status = "DONE"
            payment.save()
            serializer = PaymentSerializer(payment)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentDetail(APIView):
    def get_object(self, pk):
        try:
            return Payment.objects.get(pk=pk)
        except Payment.DoesNotExist:
            raise None

    def get(self, request, pk):
        payment = self.get_object(pk)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data)

    def put(self, request, pk):
        payment = self.get_object(pk)
        serializer = PaymentSerializer(payment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        payment = self.get_object(pk)
        payment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
