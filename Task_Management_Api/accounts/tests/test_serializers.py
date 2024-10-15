from django.contrib.auth.models import User

from ..serializers import UserSerializer
from .test_setup import TestAccountSetUp

class TestAccountSerializers(TestAccountSetUp):

    def test_user_serializer(self):
        self.serializer = UserSerializer(instance=self.user)

        data = self.serializer.data

        self.assertEqual(set(data.keys()), {'id', 'username', 'email'})
        self.assertEqual(data.get("username"), self.user.username)
        self.assertEqual(data.get("email"), self.user.email)
