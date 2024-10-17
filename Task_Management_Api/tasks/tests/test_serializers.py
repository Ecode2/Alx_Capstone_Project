from ..serializers import TaskSerializer, TaskHistorySerializer, TaskStatusSerializer
from .test_setup import TestTaskSetUp
from rest_framework.exceptions import ValidationError
import datetime

class TestTaskSerializers(TestTaskSetUp):

    def test_task_serializer(self):
        self.serializer = TaskSerializer(instance=self.task)

        data = self.serializer.data

        self.assertEqual(set(data.keys()), {"id", "Title", "Description", "DueDate", "category", "PriorityLevel", "Status", "completed_at", "author"})
        self.assertEqual(data.get("Title"), self.task.Title)

    def test_task_serializer_due_date_validation(self):
        invalid_due_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)
        serializer = TaskSerializer(data={
            "Title": "Test Task",
            "Description": "Test Description",
            "DueDate": invalid_due_date,
            "PriorityLevel": 1,
            "category": self.category.id,
            "author": self.user.id
        })

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_task_status_serializer(self):
        self.serializer = TaskStatusSerializer(instance=self.task)

        data = self.serializer.data

        self.assertEqual(set(data.keys()), set())

    def test_task_history_serializer(self):
        self.serializer = TaskHistorySerializer(instance=self.task_history)

        data = self.serializer.data

        self.assertEqual(set(data.keys()), {"id", "task", "author", "completed_at"})
        self.assertEqual(data.get("task"), str(self.task_history.task))
        self.assertEqual(data.get("author"), str(self.task_history.author))
