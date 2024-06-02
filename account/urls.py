from django.urls import path, include
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # # =========== Rest API ==================
    # path('basic/', StudentView.as_view()),
    # path('basic/<int:id>/', StudentView.as_view()),

    # # ========== Serializer Use Case =================
    # path('student/', views.student_list, name='student_list'),
    # path('student/<int:pk>/', views.student_detail, name='student_detail'),

]

if settings.DEBUG:  # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)