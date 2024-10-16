from ..models import Notification
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .test_setup import TestNotificationSetUp


class TestNotificationViews(TestNotificationSetUp):

    def test_1_list_notifications(self):
        response = self.client.get(self.list_create_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(set(response.data), {"count", "next", "previous", "results"})
        self.assertIsNotNone(response.data.get("results"))
        self.assertIsInstance(response.data.get("results"), list)

    def test_2_list_notifications_with_no_authentication(self):
        self.client.credentials()
        response = self.client.get(self.list_create_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)

    def test_3_retrieve_notification(self):
        response = self.client.get(self.crud_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(set(response.data), {'id', "actor",'recipient', 'verb', "target", 'is_read', 'timestamp'})
        self.assertEqual(response.data.get("id"), self.notification.id)

    def test_4_retrieve_notification_with_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer invalidtoken")
        response = self.client.get(self.crud_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)

    def test_5_delete_notification(self):
        response = self.client.delete(self.crud_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Notification.objects.filter(id=self.notification.id).exists())

    def test_6_list_read_notifications(self):
        response = self.client.get(self.read_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(set(response.data), {"count", "next", "previous", "results"})
        self.assertIsNotNone(response.data.get("results"))
        self.assertIsInstance(response.data.get("results"), list)

    def test_7_list_unread_notifications(self):
        response = self.client.get(self.unread_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(set(response.data), {"count", "next", "previous", "results"})
        self.assertIsNotNone(response.data.get("results"))
        self.assertIsInstance(response.data.get("results"), list)

    def test_8_mark_all_as_read(self):
        response = self.client.post(self.read_all_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("detail"), "All notifications marked as read")
        self.assertTrue(Notification.objects.filter(recipient=self.user, is_read=True).exists())

    def test_9_mark_all_as_unread(self):
        response = self.client.post(self.unread_all_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("detail"), "All notifications marked as unread")
        self.assertTrue(Notification.objects.filter(recipient=self.user, is_read=False).exists())
