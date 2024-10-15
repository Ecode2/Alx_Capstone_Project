from django.contrib.auth.models import User
from .test_setup import TestAccountSetUp

class TestAccountModels(TestAccountSetUp):

    def test_user_creation(self):

        user_data = {
            "username": self.fake.name().strip(),
            "email": self.fake.email(domain="gmail.com"),
            "password": self.fake.password(length=10)
        }

        user = User.objects.create(**user_data)

        self.assertIsInstance(user, User)

        self.assertEqual(user.username, user_data.get("username"))
        self.assertEqual(user.email, user_data.get("email"))

        self.assertNotEqual(user.username, "Doe")

        self.assertEqual(User.objects.get(username=user_data.get("username"), email=user_data.get("email")),
                         user)