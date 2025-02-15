from django.urls import path, include
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # # =========== Message API ==================
    path('user/messages/', MessageListAPIView.as_view()),
    path('user/messages/<int:pk>/', MessageDetailAPIView.as_view()),
]
