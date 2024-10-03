from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, response, status
from django.contrib.auth import login, authenticate, logout
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User
from .serializers import UserSerializer, PublicUserSerializer

#permissions.IsAuthenticated", "return Response

# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, username=username, email=email, password=password)
        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return response.Response({"token": token.key, 
                                      "token_type": "Token"})
        else:
            return response.Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        
class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PublicUserSerializer

    def get_object(self):
        return self.request.user
    