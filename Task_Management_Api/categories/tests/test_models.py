
from ..models import Category
from .test_setup import TestCategorySetUp

class TestCategoryModels(TestCategorySetUp):

    def test_category_creation_with_author(self):
        category = Category.objects.create(**self.category_data)

        self.assertIsInstance(category, Category)
        self.assertEqual(category.name, self.category_data.get("name"))
        self.assertEqual(category.author, self.user)

        self.assertEqual(category.author.username, "Jane")
        self.assertEqual(Category.objects.get(name=self.category_data.get("name")).author, self.user)

    def test_category_creation_without_author(self):
        category = Category.objects.create(name=self.category_data.get("name"))

        self.assertIsInstance(category, Category)

        self.assertEqual(category.name, self.category_data.get("name"))
        self.assertEqual(category.author, None)
        self.assertEqual(Category.objects.get(name=self.category_data.get("name")).name, self.category_data.get("name"))