from django.urls import path, include, reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import URLPatternsTestCase

from .test_setup import TestAccountSetUp

class TestAccountUrls(TestAccountSetUp, URLPatternsTestCase):
    urlpatterns = [
        path('accounts/', include('accounts.urls')),
    ]

    def test_profile_url(self):
        response = self.client.get(self.profile_url)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_register_url(self):
        response = self.client.post(self.register_url)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_login_url(self):
        response = self.client.post(self.login_url)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_token_refresh_url(self):
        response = self.client.post(self.refresh_url)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_token_verify_url(self):
        response = self.client.post(self.verify_url)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)