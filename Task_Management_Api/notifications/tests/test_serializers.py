from ..serializers import NotificationSerializer
from .test_setup import TestNotificationSetUp


class TestNotificationSerializers(TestNotificationSetUp):

    def test_user_serializer(self):
        self.serializer = NotificationSerializer(instance=self.notification)

        data = self.serializer.data

        self.assertEqual(set(data.keys()), {"id", "actor", "recipient", "verb", "target", "is_read", "timestamp"})
        self.assertEqual(data.get("verb"), self.notification.verb)
