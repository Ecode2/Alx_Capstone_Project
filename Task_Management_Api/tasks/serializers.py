from rest_framework.serializers import ModelSerializer, StringRelatedField, ValidationError
import datetime

from .models import Task

class TaskSerializer(ModelSerializer):
    author = StringRelatedField()

    class Meta:
        model = Task
        fields = ["id", "Title", "Description", "DueDate", "PriorityLevel", "Status", "completed_at", "author"]
        read_only_fields = ["id", "completed_at", "Status"]

    def validate_DueDate(self, value):
        current_date = datetime.datetime.now(datetime.UTC)
        due_date = value

        if due_date and due_date <= current_date:
            raise ValidationError("due date can not be in the past")
        return value

class CompleteTaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = []