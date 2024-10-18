import pdb
from ..models import Task, TaskHistory
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .test_setup import TestTaskSetUp


class TestTaskViews(TestTaskSetUp):

    def test_1_create_task(self):
        task_data = self.task_data.copy()
        task_data.pop("author")
        response = self.client.post(self.list_create_url, task_data)
        pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("Title"), self.task_data["Title"])
        self.assertEqual(response.data.get("Description"), self.task_data["Description"])

    def test_2_list_tasks(self):
        response = self.client.get(self.list_create_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(set(response.data), {"count", "next", "previous", "results"})
        self.assertIsNotNone(response.data.get("results"))
        self.assertIsInstance(response.data.get("results"), list)

    def test_3_retrieve_task(self):
        response = self.client.get(self.crud_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(set(response.data), {"id", "Title", "Description", "DueDate", "category", "PriorityLevel",
                                              "Status", "completed_at", "author"})
        self.assertEqual(response.data.get("id"), self.task.id)

    def test_4_update_task(self):
        task_data = {
            "Title": "Updated Task",
            "Description": "Updated description",
            "DueDate": "2024-11-01T00:00:00Z"
        }
        response = self.client.patch(self.crud_url, task_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("Title"), task_data["Title"])
        self.assertEqual(response.data.get("Description"), task_data["Description"])

    def test_5_delete_task(self):
        response = self.client.delete(self.crud_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_6_toggle_task_status(self):
        response = self.client.post(self.complete_toggle_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.Status, "COMPLETED")

        response = self.client.post(self.complete_toggle_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.Status, "PENDING")

    def test_7_list_task_history(self):
        TaskHistory.objects.create(task=self.task2, author=self.user, completed_at="2024-11-01T00:00:00Z")
        response = self.client.get(self.history_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(set(response.data), {"count", "next", "previous", "results"})
        self.assertIsNotNone(response.data.get("results"))
        self.assertIsInstance(response.data.get("results"), list)
