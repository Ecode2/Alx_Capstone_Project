from django.urls import path, include, reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import URLPatternsTestCase

from .test_setup import TestCategorySetUp


class TestCategoryUrls(TestCategorySetUp, URLPatternsTestCase):
    urlpatterns = [
        path("category/", include("categories.urls")),
    ]

    def test_list_create_url(self):
        response = self.client.get(self.list_create_url)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_crud_url(self):
        response = self.client.get(self.crud_url)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)