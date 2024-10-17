from rest_framework import serializers
from .models import Notification


class GenericRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return str(value)
    
    def to_internal_value(self, data):
        model_class = self.queryset.model
        try:
            return model_class.objects.get(pk=data)
        except model_class.DoesNotExist:
            return serializers.ValidationError(f"Object with pk={data} does not exist.")

class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Notification model.
    This serializer converts Notification model instances into JSON format and vice versa.
    It includes the following fields:
    - id: The unique identifier for the notification (read-only).
    - actor: The user who performed the action that generated the notification.
    - recipient: The user who is the target of the notification.
    - verb: A short description of the action that generated the notification.
    - target: The object that the action was performed on.
    - is_read: A boolean indicating whether the notification has been read.
    - timestamp: The time when the notification was created (read-only).
    Meta:
        model (Notification): The model that is being serialized.
        fields (list): The fields to include in the serialized output.
        read_only_fields (list): The fields that should be read-only.
    """
    target = GenericRelatedField(read_only=True)
    class Meta:
        model=Notification
        fields = ["id", "actor", "recipient", "verb", "target", "is_read", "timestamp"]
        read_only_fields = ['id', "actor",  "verb", "recipient", "is_read", 'timestamp']
