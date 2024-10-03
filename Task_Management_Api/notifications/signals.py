from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from .models import Notification


class Notify:

    @staticmethod
    def send(actor, recipient, verb, target):
        target_content_type = ContentType.objects.get_for_model(target)
        target_object_id = target.pk

        notification = Notification.objects.create(
            recipient=recipient,
            actor=actor,
            target_content_type = target_content_type,
            target_object_id=target_object_id,
        )
        return notification

    @staticmethod
    def read(notification: Notification):
        notification.is_read = True
        notification.save()

    @staticmethod
    def mark_all_as_read(user:User):
        user.notifications.update(is_read=True)

    @staticmethod
    def mark_all_as_unread(user:User):
        user.notifications.update(is_read=False)
    
    @staticmethod
    def get_read_notifications(user):
        return Notification.objects.filter(recipient=user, is_read=True)
    
    @staticmethod
    def get_unread_notifications(user):
        return Notification.objects.filter(recipient=user, is_read=False)
    