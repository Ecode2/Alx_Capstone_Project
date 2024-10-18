import pdb
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from ..models import Notification
from ..signals import Notify
from .test_setup import TestNotificationSetUp

class TestNotificationSignals(TestNotificationSetUp):

    def setUp(self):
        super().setUp()
        self.actor = User.objects.create(username='actor')
        self.recipient = User.objects.create(username='recipient')
        self.target = User.objects.create(username='target')
        self.verb = 'liked'

    def test_send_notification(self):
        notification = Notify.send(self.actor, self.recipient, self.verb, self.target)
        
        self.assertIsInstance(notification, Notification)
        self.assertEqual(notification.actor, self.actor)
        self.assertEqual(notification.recipient, self.recipient)
        self.assertEqual(notification.verb, self.verb)
        self.assertEqual(notification.target_object_id, self.target.pk)
        self.assertEqual(notification.target_content_type, ContentType.objects.get_for_model(self.target))

    def test_read_notification(self):
        notification = Notify.send(self.actor, self.recipient, self.verb, self.target)
        Notify.read(notification)
        notification.refresh_from_db()
        self.assertTrue(notification.is_read)

    def test_mark_all_as_read(self):
        Notify.send(self.actor, self.recipient, self.verb, self.target)
        Notify.send(self.actor, self.recipient, self.verb, self.target)
        Notify.mark_all_as_read(self.recipient)
        notifications = Notification.objects.filter(recipient=self.recipient)
        for notification in notifications:
            self.assertTrue(notification.is_read)

    def test_mark_all_as_unread(self):
        Notify.send(self.actor, self.recipient, self.verb, self.target)
        Notify.send(self.actor, self.recipient, self.verb, self.target)
        Notify.mark_all_as_read(self.recipient)
        Notify.mark_all_as_unread(self.recipient)
        notifications = Notification.objects.filter(recipient=self.recipient)
        for notification in notifications:
            self.assertFalse(notification.is_read)

    def test_get_read_notifications(self):
        Notify.send(self.actor, self.recipient, self.verb, self.target)
        notification = Notify.send(self.actor, self.recipient, self.verb, self.target)
        Notify.read(notification)
        read_notifications = Notify.get_read_notifications(self.recipient)
        self.assertIn(notification, read_notifications)
        self.assertEqual(read_notifications.count(), 1)

    def test_get_unread_notifications(self):
        Notify.send(self.actor, self.recipient, self.verb, self.target)
        unread_notifications = Notify.get_unread_notifications(self.recipient)
        self.assertEqual(unread_notifications.count(), 1)
        for notification in unread_notifications:
            self.assertFalse(notification.is_read)