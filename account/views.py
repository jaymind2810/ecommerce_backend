from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token 
from rest_framework.permissions import IsAuthenticated 
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login  # For login functionality

from .serializers import (
    CustomTokenObtainPairSerializer,
    UserSerializer,
    RegisterSerializer
)
from .models import User  # Import your User model (if not using Django's default)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from .utils import (
    getAllUsers,
    getUserAllData,
    getAllHomePageData,
    registerUser,
    validateUserLoginData
)

class CustomTokenObtainPairView(TokenObtainPairView):
    # Login Validattion
    serializer_class = CustomTokenObtainPairSerializer

class UserRegistrationAPIView(APIView):
    """
    API endpoint for user registration.
    """
    def post(self, request):
        try:
            response = registerUser(request)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        

class UserLoginAPIView(APIView):
    """
    API endpoint for user login.
    """
    def post(self, request, format=None):
        try:
            response = validateUserLoginData(request)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)


class UserRetrieveUpdateAPIView(APIView):
    """
    API endpoint for retrieving and updating a user's profile.
    Requires authentication.
    """

    permission_classes = [IsAuthenticated]  # Only authenticated users can access

    def get_object(self, request):
        return request.user  # Retrieve the authenticated user

    def get(self, request, format=None):
        user = self.get_object(request)
        serializer = UserSerializer(user)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        user = self.get_object(request)
        serializer = UserSerializer(user, data=request.data, partial=True)  # Allow partial updates
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def getAllData(self, pk):
    try:
        response = getUserAllData(pk)
        return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
    
class UserListAllData(APIView):
    # permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            response = getAllUsers(request)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
    

class HomePageAllData(APIView):
    # permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            response = getAllHomePageData(request)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
