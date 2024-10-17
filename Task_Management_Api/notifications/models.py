from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


# Create your models here.
class Notification(models.Model):
    """
    Notification model to represent notifications in the system.
    Attributes:
        recipient (ForeignKey): The user who receives the notification.
        actor (ForeignKey): The user who performs the action that triggers the notification.
        verb (TextField): A description of the action performed by the actor.
        target_content_type (ForeignKey): The content type of the target object.
        target_object_id (PositiveIntegerField): The ID of the target object.
        target (GenericForeignKey): A generic foreign key to the target object.
        is_read (BooleanField): A flag indicating whether the notification has been read.
        timestamp (DateTimeField): The time when the notification was created.
    Methods:
        __str__: Returns a string representation of the notification.
    """
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications_created")

    verb = models.TextField()

    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='target_obj')
    target_object_id = models.PositiveIntegerField()
    target = GenericForeignKey('target_content_type', 'target_object_id')
    is_read = models.BooleanField(default=False)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.actor} {self.verb} {self.target}"
    
    class Meta:
        ordering = ["-timestamp"]