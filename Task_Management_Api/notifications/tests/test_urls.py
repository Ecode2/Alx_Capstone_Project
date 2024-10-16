from django.urls import path, include, reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import URLPatternsTestCase

from .test_setup import TestNotificationSetUp


class TestNotificationUrls(TestNotificationSetUp, URLPatternsTestCase):
    urlpatterns = [
        path("notifications/", include("notifications.urls")),
    ]

    def test_list_create_url(self):
        response = self.client.get(self.list_create_url)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_crud_url(self):
        response = self.client.get(self.crud_url)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_read_notifications_url_post(self):
        response = self.client.get(self.read_url)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unread_notifications_url_post(self):
        response = self.client.get(self.unread_url)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_read_all_notifications_url_post(self):
        response = self.client.get(self.read_all_url)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unread_all_notifications_url_post(self):
        response = self.client.get(self.unread_all_url)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)