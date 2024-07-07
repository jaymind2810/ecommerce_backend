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

]

if settings.DEBUG:  # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
