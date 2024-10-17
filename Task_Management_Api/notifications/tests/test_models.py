
from ..models import Notification
from .test_setup import TestNotificationSetUp

class TestNotificationModels(TestNotificationSetUp):

    def test_notification_creation(self):
        notification = Notification.objects.create(target=self.category, **self.notification_data)

        self.assertIsInstance(notification, Notification)
        self.assertEqual(notification.verb, self.notification_data.get("verb"))
        self.assertEqual(notification.actor, self.admin_user)
