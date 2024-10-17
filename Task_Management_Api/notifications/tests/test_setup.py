import pdb
from faker import Faker
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from categories.models import Category
from ..models import Notification


class TestNotificationSetUp(APITestCase):

    def setUp(self):
        super().setUp()

        self.fake = Faker()

        self.list_create_url = reverse("list_create_notifications")
        self.read_url = reverse("read_notifications")
        self.unread_url = reverse("unread_notifications")
        self.read_all_url = reverse("read_all_notifications")
        self.unread_all_url = reverse("unread_all_notifications")

        self.admin_user = User.objects.create_superuser(username="John", email="johnDoe@gmailcom", password="johnDoe")
        self.user = User.objects.create_user(username="Jane", email="janeDoe@gmailcom", password="janeDoe")
        self.user2 = User.objects.create_user(username="Jones", email="jonesDoe@gmailcom", password="jonesDoe")

        self.notification_data = {
            "actor": self.admin_user,
            "recipient": self.user,
            "verb": self.fake.sentence(),
        }

        self.category = Category.objects.create(name="Test Category", author=self.user)
        self.notification = Notification.objects.create(actor=self.admin_user, recipient=self.user, verb=f"New category created", target=self.category)
        self.crud_url = reverse("detail_notification", args=[self.notification.id])

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
