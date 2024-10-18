import pdb
from django.urls import path, include, reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import URLPatternsTestCase

from .test_setup import TestTaskSetUp


class TestTaskUrls(TestTaskSetUp, URLPatternsTestCase):
    urlpatterns = [
        path("tasks/", include("tasks.urls")),
    ]

    def test_list_create_task_url(self):
        response = self.client.get(self.list_create_url)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_crud_task_url(self):
        response = self.client.get(self.crud_url)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_task_completion_toggle_url(self):
        response = self.client.get(self.complete_toggle_url)

        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_task_history_url(self):
        response = self.client.get(self.history_url)

        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)