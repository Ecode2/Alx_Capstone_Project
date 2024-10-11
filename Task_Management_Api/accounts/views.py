from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, response, status
from django.contrib.auth import login, authenticate, logout

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
    