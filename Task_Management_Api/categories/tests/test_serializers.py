from django.contrib.auth.models import User

from ..serializers import CategorySerializer
from .test_setup import TestCategorySetUp


class TestCategorySerializers(TestCategorySetUp):

    def test_user_serializer(self):
        self.serializer = CategorySerializer(instance=self.category)

        data = self.serializer.data

        self.assertEqual(set(data.keys()), {'id', 'name'})
        self.assertEqual(data.get("name"), "Work")
