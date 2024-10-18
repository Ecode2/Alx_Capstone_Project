import pdb

from ..models import Task, TaskHistory
from .test_setup import TestTaskSetUp


class TestTaskModels(TestTaskSetUp):

    def test_task_creation(self):
        task = Task.objects.create(**self.task_data)

        self.assertIsInstance(task, Task)
        self.assertEqual(task.Title, self.task_data.get("Title"))
        self.assertEqual(task.author, self.user)

    def test_task_default_priority(self):
        task_data = self.task_data.copy()
        task_data.pop('PriorityLevel')
        task = Task.objects.create(**task_data)

        self.assertEqual(task.PriorityLevel, 'LOW')

    def test_task_default_status(self):
        task_data = self.task_data.copy()
        task = Task.objects.create(**task_data)

        self.assertEqual(task.Status, 'PENDING')


class TestTaskHistoryModels(TestTaskSetUp):

    def test_task_history_creation(self):
        task = Task.objects.create(**self.task_data)
        task_history = TaskHistory.objects.create(task=task, author=self.user)

        self.assertIsInstance(task_history, TaskHistory)
        self.assertEqual(task_history.task, task)
        self.assertEqual(task_history.author, self.user)
