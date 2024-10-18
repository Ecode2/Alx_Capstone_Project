from rest_framework.serializers import (ModelSerializer, StringRelatedField, ValidationError)
import datetime
from django.db import models

from categories.models import Category
from .models import Task, TaskHistory


from rest_framework.relations import PrimaryKeyRelatedField

class UserCategoryRelatedField(PrimaryKeyRelatedField):
    def get_queryset(self):
        request = self.context.get('request', None)
        queryset = super().get_queryset()

        if request is None:
            return Category.objects.none()

        # Filter the queryset to include only general categories and categories created by the current user
        return queryset.filter(
            models.Q(author__isnull=True) | models.Q(author=request.user)
        )


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
    author = StringRelatedField(read_only=True)
    category = UserCategoryRelatedField(queryset=Category.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Task
        fields = ["id", "Title", "Description", "DueDate", "category", "PriorityLevel", "Status",
                  "completed_at", "author"]
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
    """
    TaskHistorySerializer is a ModelSerializer for the TaskHistory model.

    Fields:
        - id: Integer, read-only
        - task: String
        - author: String, related field
        - completed_at: DateTime, read-only
    """
    class Meta:
        model=TaskHistory
        fields = ["id", "task", "author", "completed_at"]
        read_only_fields = ["id", "completed_at"]