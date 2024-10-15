import pdb
from faker import Faker
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken


class TestAccountSetUp(APITestCase):

    def setUp(self):
        
        super().setUp()
    
        self.fake = Faker()

        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.refresh_url = reverse("token_refresh")
        self.verify_url = reverse("token_verify")
        self.profile_url = reverse("profile")

        name =self.fake.name().split()
        name = "".join(name)
        self.user_data = {
            "username": name,
            "email": self.fake.email(domain="gmail.com"),
            "password": self.fake.password(length=10)
        }

        self.user = User.objects.create_user(username="John", email="johnDoe@gmailcom", password="johnDoe")
        self.login_data = {
            "username": "John",
            "password": "johnDoe"
        }

        tokens = RefreshToken.for_user(self.user)
        self.access_token = str(tokens.access_token)
        self.refresh_token = str(tokens)
        
        self.client = APIClient(enforce_csrf_checks = True)