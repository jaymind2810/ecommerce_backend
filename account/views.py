
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token  # For token-based authentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated  # Permission for authenticated users

from django.contrib.auth import authenticate, login  # For login functionality

from .serializers import UserSerializer  # Import your UserSerializer
from .models import User  # Import your User model (if not using Django's default)

class UserRegistrationAPIView(APIView):
    """
    API endpoint for user registration.
    """

    def post(self, request, format=None):
        data = request.data
        del data["password2"]
        email = data['email']
        data['username'] = email
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(APIView):
    """
    API endpoint for user login.
    """

    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        
        print(username, password, "=======UserName========")
        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        print(user, "==user00000")
        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)  # Log in the user
        token, _ = Token.objects.get_or_create(user=user)  # Generate a token (if using token-based auth)
        return Response({'token': token.key}, status=status.HTTP_200_OK)  # Return the token

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