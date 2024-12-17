from django.urls import path, include
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    # ============= JWT Authentication Login Api================

    # path('token/', jwt_views.TokenObtainPairView.as_view(), name ='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name ='token_refresh'),
    path('auth/register/', UserRegistrationAPIView.as_view(), name='register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('auth/logout/', LogoutView.as_view(), name='logout'),

    # ============= Users Api================
    path('auth/user/', UserRetrieveUpdateAPIView.as_view(), name='user_profile'),
    path('auth/getuseralldata/<int:pk>/', getAllData, name='getAllData'),

    # =============== HomePage WebPanel Api ================
    path('homePage/allData/', HomePageAllData.as_view()),


]

if settings.DEBUG:  # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)