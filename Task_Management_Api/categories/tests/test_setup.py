import pdb
from faker import Faker
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from ..models import Category


class TestCategorySetUp(APITestCase):

    def setUp(self):
        super().setUp()

        self.fake = Faker()

        self.list_create_url = reverse("list_create_category")

        self.admin_user = User.objects.create_superuser(username="John", email="johnDoe@gmailcom", password="johnDoe")
        self.user = User.objects.create_user(username="Jane", email="janeDoe@gmailcom", password="janeDoe")
        self.user2 = User.objects.create_user(username="Jones", email="jonesDoe@gmailcom", password="jonesDoe")

        category_name = self.fake.color()
        self.category_data = {
            "name": category_name,
            "author": self.user
        }

        self.category = Category.objects.create(name="Work")
        
        self.user_category = Category.objects.create(name="User Category", author=self.user)
        self.crud_url = reverse("read_update_delete_category", args=[self.user_category.id])

        admin_token = RefreshToken.for_user(self.user)
        self.admin_access_token = str(admin_token.access_token)

        token1 = RefreshToken.for_user(self.user)
        self.access_token1 = str(token1.access_token)

        token2 = RefreshToken.for_user(self.user2)
        self.access_token2 = str(token2.access_token)

        self.client = APIClient(enforce_csrf_checks=True)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token1)

    def tearDown(self):
        return super().tearDown()