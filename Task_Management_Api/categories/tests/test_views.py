import pdb
from ..models import Category
from rest_framework import status
 
from .test_setup import TestCategorySetUp


class TestCategoryViews(TestCategorySetUp):

    def test_1_create_new_category(self):
        response = self.client.post(self.list_create_url, {"name": self.category_data.get("name")})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(set(response.data), {'id', 'name'})
        self.assertEqual(response.data.get("name"), self.category_data.get("name"))
        self.assertEqual(Category.objects.get(name=self.category_data.get("name")).author.username, "Jane")

    def test_2_create_new_default_category(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.admin_access_token)
        response = self.client.post(self.list_create_url, {"name": self.category_data.get("name")})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(set(response.data), {'id', 'name'})
        self.assertEqual(response.data.get("name"), self.category_data.get("name"))  

    def test_3_list_default_and_user_created_categories(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.admin_access_token)
        response = self.client.get(self.list_create_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(set(response.data), {"count","next","previous","results"})
        self.assertIsNotNone(response.data.get("results"))
        self.assertIsInstance(response.data.get("results"), list)  

    def test_4_create_new_category_with_missing_name(self):
        response = self.client.post(self.list_create_url, {"name": ""})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)

    def test_5_list_categories_with_no_authentication(self):
        self.client.credentials()
        response = self.client.get(self.list_create_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)

    def test_6_create_new_category_with_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer invalidtoken")
        response = self.client.post(self.list_create_url, {"name": self.category_data.get("name")})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)

    def test_7_retrieve_category(self):
        response = self.client.get(self.crud_url.format(self.category.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(set(response.data), {'id', 'name'})
        self.assertEqual(response.data.get("name"), self.user_category.name)

    def test_8_update_category(self):
        response = self.client.put(self.crud_url, {"name": "Updated Category"})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), "Updated Category")
        self.assertEqual(Category.objects.get(id=self.user_category.id).name, "Updated Category")

    def test_9_partial_update_category(self):
        response = self.client.patch(self.crud_url, {"name": "Partially Updated Category"})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("name"), "Partially Updated Category")
        self.assertEqual(Category.objects.get(id=self.user_category.id).name, "Partially Updated Category")

    def test_99_delete_category(self):
        response = self.client.delete(self.crud_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(id=self.user_category.id).exists())