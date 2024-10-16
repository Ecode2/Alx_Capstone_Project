import pdb
from faker import Faker
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from categories.models import Category
from ..models import Task, TaskHistory


class TestTaskSetUp(APITestCase):

    def setUp(self):
        super().setUp()

        self.fake = Faker()

        self.list_create_url = reverse("list_create_task")
        self.crud_url = reverse("read_update_delete_task", args=[1])
        self.complete_toggle_url = reverse("toggle_complete_pending_task", args=[1])
        self.history_url = reverse("task_history")

        self.admin_user = User.objects.create_superuser(username="John", email="johnDoe@gmailcom", password="johnDoe")
        self.user = User.objects.create_user(username="Jane", email="janeDoe@gmailcom", password="janeDoe")
        self.user2 = User.objects.create_user(username="Jones", email="jonesDoe@gmailcom", password="jonesDoe")

        self.task_data = {
            "Title": self.fake.sentence(),
            "Description": self.fake.text(),
            "PriorityLevel": "LOW",
            "author": self.user,
            'DueDate': "2025-10-18T10:17:44.759Z"
        }

        self.category = Category.objects.create(name="Work", author=self.user)
        self.task = Task.objects.create(Title="Test Task", Description="Test Description", author=self.user,
                                        DueDate="2025-11-18T10:17:44.759Z",
                                        category=self.category)
        self.task2 = Task.objects.create(Title="Test Task two", Description="Test Description two", author=self.user,
                                         DueDate="2025-12-18T10:17:44.759Z",
                                         category=self.category)

        self.task_history = TaskHistory.objects.create(task=self.task, author=self.user)
        self.task_history2 = TaskHistory.objects.create(task=self.task2, author=self.user)

        self.crud_url = reverse("read_update_delete_task", args=[self.task.id])
        self.complete_toggle_url = reverse("toggle_complete_pending_task", args=[self.task.id])

        admin_token = RefreshToken.for_user(self.admin_user)
        self.admin_access_token = str(admin_token.access_token)

        token1 = RefreshToken.for_user(self.user)
        self.access_token1 = str(token1.access_token)

        token2 = RefreshToken.for_user(self.user2)
        self.access_token2 = str(token2.access_token)

        self.client = APIClient(enforce_csrf_checks=True)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token1)

    def tearDown(self):
        return super().tearDown()
