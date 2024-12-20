from django.urls import path, include
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # # =========== Product API ==================
    path('api/create-payment-intent/', create_payment, name='create_payment'),
    # path('api/config', views.get_config, name='config'),
    # path('api/create-payment-intent', views.create_payment, name='create-payment-intent'),
    # path('api/payment/next', views.get_payment_next, name='payment-next'),
    # path('api/success', views.get_success, name='success'),
    # path('api/webhook', views.webhook_received, name='webhook'),

    # ============ Cart API =========================
    path('cart-items/', CartItemListAPIView.as_view(), name='cartitem-list-create'),
    path('cart-items/<int:pk>/', CartItemDetailAPIView.as_view(), name='cartitem-detail'),

    # ============ Addresss ========================
    path('address/', AddressListAPIView.as_view(), name='address-list-create'),
    path('address/<int:pk>/', AddressDetailAPIView.as_view(), name='address-detail'),

]

if settings.DEBUG:  # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
