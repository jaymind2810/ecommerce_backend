from django.urls import path, include
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # # =========== Rest API ==================
    path('auth/register/', UserRegistrationAPIView.as_view()),
    path('auth/login/', UserLoginAPIView.as_view()),

]

if settings.DEBUG:  # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)