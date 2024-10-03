from rest_framework import serializers

from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Notification
        fields = ["id", "actor", "recipient", "verb", "target", "is_read", "timestamp"]
        read_only_fields = ['id', 'timestamp']