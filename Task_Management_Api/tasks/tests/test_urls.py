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
        response = self.client.get(self.list_create_task_url)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_crud_task_url(self):
        response = self.client.get(self.crud_task_url)
        pdb.set_trace()
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_read_task_url_post(self):
        response = self.client.get(self.read_task_url)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unread_task_url_post(self):
        response = self.client.get(self.unread_task_url)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_read_all_tasks_url_post(self):
        response = self.client.get(self.read_all_tasks_url)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unread_all_tasks_url_post(self):
        response = self.client.get(self.unread_all_tasks_url)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)