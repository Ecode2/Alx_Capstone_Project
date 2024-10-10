from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, response, status
from django.contrib.auth import login, authenticate, logout
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User
from .serializers import UserSerializer, PublicUserSerializer

# Create your views here.
class RegisterView(generics.CreateAPIView):
    """
    RegisterView is a generic API view for creating new user accounts.

    This view allows any user to register by providing the necessary user details.
    It uses the UserSerializer to validate and save the user data.

    Attributes:
        queryset (QuerySet): A queryset of all User objects.
        serializer_class (Serializer): The serializer class used for validating and saving user data.
        permission_classes (list): A list of permission classes that determine access to this view.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(generics.GenericAPIView):
    """
    LoginView handles user authentication and token generation.

    Attributes:
        serializer_class (UserSerializer): Serializer class for user data.
        permission_classes (list): List of permission classes, allowing any user to access this view.

    Methods:
        post(request, *args, **kwargs):
            Authenticates the user with the provided username, email, and password.
            If authentication is successful, logs in the user and returns a token.
            If authentication fails, returns an error response with status 400.
            
            Parameters:
                request (Request): The HTTP request object containing user credentials.
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.
            
            Returns:
                Response: A response object containing the authentication token or an error message.

    Permissions:
        - AllowAny: permission to allow anyone to login.
    """
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
    """
    ProfileView is a view for retrieving, updating, and deleting the profile of the currently authenticated user.

    Attributes:
        serializer_class (PublicUserSerializer): The serializer class used for validating and deserializing input, and for serializing output.

    Methods:
        get_object(self):
            Returns the currently authenticated user.
    """
    serializer_class = PublicUserSerializer

    def get_object(self):
        return self.request.user
    