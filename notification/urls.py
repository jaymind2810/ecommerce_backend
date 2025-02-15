from django.urls import path, include
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # # =========== Orders API ==================
    # path('orders/', OrderListAPIView.as_view()),
    # path('orders/<int:pk>/', OrderDetailAPIView.as_view()),

]
