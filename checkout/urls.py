from django.urls import path, include
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # ============ Cart API =========================
    path('cart-items/', CartItemListAPIView.as_view(), name='cartitem-list-create'),
    path('cart-items/<int:pk>/', CartItemDetailAPIView.as_view(), name='cartitem-detail'),

    # ============ Addresss ========================
    path('address/', AddressListAPIView.as_view(), name='address-list-create'),
    path('address/<int:pk>/', AddressDetailAPIView.as_view(), name='address-detail'),

]

if settings.DEBUG:  # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
