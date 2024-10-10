"""
URL configuration for the accounts app.

This module defines the URL patterns for the accounts-related views, including
registration, login, and profile management.

Routes:
- /register/ : RegisterView (name='register')
- /login/ : LoginView (name='login')
- /profile/ : ProfileView (name='profile')

Imports:
- path: Function to define URL patterns.
- views: Importing local views from the current directory.
"""
from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
]