from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from .models import Notification


class Notify:
    """
    Notify class provides static methods to handle notification-related operations.
    Methods:
    """

    @staticmethod
    def send(actor, recipient, verb, target):
        """ send(actor, recipient, verb, target): 
        Sends a notification to the recipient with the specified actor, verb, and target. """
        target_content_type = ContentType.objects.get_for_model(target)
        target_object_id = target.pk

        notification = Notification.objects.create(
            recipient=recipient,
            actor=actor,
            verb=verb,
            target_content_type = target_content_type,
            target_object_id=target_object_id,
        )
        return notification

    @staticmethod
    def read(notification: Notification):
        """read(notification: Notification): 
        Marks the specified notification as read."""
        notification.is_read = True
        notification.save()

    @staticmethod
    def mark_all_as_read(user:User):
        """mark_all_as_read(user: User):
        Marks all notifications for the specified user as read."""
        user.notifications.update(is_read=True)

    @staticmethod
    def mark_all_as_unread(user:User):
        """mark_all_as_unread(user: User):
        Marks all notifications for the specified user as unread."""
        user.notifications.update(is_read=False)
    
    @staticmethod
    def get_read_notifications(user):
        """get_read_notifications(user):
        Retrieves all read notifications for the specified user."""
        return Notification.objects.filter(recipient=user, is_read=True)
    
    @staticmethod
    def get_unread_notifications(user):
        """get_unread_notifications(user):
        Retrieves all unread notifications for the specified user."""
        return Notification.objects.filter(recipient=user, is_read=False)
    