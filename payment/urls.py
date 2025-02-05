from django.urls import path, include
from rest_framework import routers
from .views import *


urlpatterns = [
    path('payments/create/', AllPaymentItemListCreate.as_view(), name='allpayment-list-create'),
    path('payments/', PaymentListCreate.as_view(), name='payment-list-create'),
    path('payments/<int:pk>/', PaymentDetail.as_view(), name='payment-detail'),
    # -------Stripe -------------
    path('api/create-stripe-customer/', create_stripe_customer, name='create_stripe_customer'),
    path('api/retrive-customer-paymentmethod/', retrive_customer_paymentMethods, name='retrive_customer_paymentMethods'),
    path('api/delete-customer-paymentmethod/', delete_customer_paymentMethods, name='delete_customer_paymentMethods'),
    path('api/create-payment-intent/', create_stripe_payment_intent, name='create_stripe_payment_intent'),
    path('api/create-stripe-payment-record/', create_stripe_payment_record, name='create_stripe_payment_record'),
    # ------------ Paypal ----------------
    path('api/create-paypal-order/', create_paypal_payment, name='create_paypal_payment'),
]