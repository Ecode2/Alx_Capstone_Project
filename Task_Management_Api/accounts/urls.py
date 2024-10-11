"""
URL configuration for the accounts app.

This module defines the URL patterns for the accounts-related views, including
registration, login, and profile management.

Routes:
- register/ : RegisterView (name='register') create a new user
- login/ : TokenObtainPairView (name='login') get access and refresh json web token
- profile/ : ProfileView (name='profile') crud operations for user
- token/refresh/: TokenRefreshView (name='token_refresh') refresh access token
- token/verify/: TokenVerifyView (name='token_verify') verify status of access token

Imports:
- path: Function to define URL patterns.
- views: Importing local views from the current directory.
"""
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name='login'),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]