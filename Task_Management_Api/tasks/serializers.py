from rest_framework.serializers import ModelSerializer, StringRelatedField, ValidationError
import datetime

from .models import Task, TaskHistory

class TaskSerializer(ModelSerializer):
    """
    TaskSerializer is a ModelSerializer for the Task model.

    Fields:
        - id: Integer, read-only
        - Title: String
        - Description: String
        - DueDate: DateTime
        - PriorityLevel: Integer
        - Status: String, read-only
        - completed_at: DateTime, read-only
        - author: String, related field
        - category: String, related field

    Methods:
        - validate_DueDate(value): Validates that the due date is not in the past.

    Raises:
        - ValidationError: If the due date is in the past.
    """
    author = StringRelatedField()
    category = StringRelatedField()

    class Meta:
        model = Task
        fields = ["id", "Title", "Description", "DueDate", "PriorityLevel", "Status", "completed_at", "author", "category"]
        read_only_fields = ["id", "completed_at", "Status"]

    def validate_DueDate(self, value):
        current_date = datetime.datetime.now(datetime.UTC)
        due_date = value

        if due_date and due_date <= current_date:
            raise ValidationError("due date can not be in the past")
        return value

class TaskStatusSerializer(ModelSerializer):
    """
    TaskStatusSerializer is a ModelSerializer for Task status.

    This serializer is used to handle the serialization and deserialization
    of Task model instances, specifically focusing on the status of the task.

    Attributes:
        Meta (class): A nested class that defines the metadata options for the serializer.
            - model (Task): The model that this serializer is associated with.
            - fields (list): The list of fields to be included in the serialization.
    """
    class Meta:
        model = Task
        fields = []

class TaskHistorySerializer(ModelSerializer):
    class Meta:
        model=TaskHistory
        fields = ["id", "task", "author", "completed_at"]