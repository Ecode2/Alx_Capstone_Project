import pdb
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
 
from .test_setup import TestAccountSetUp

class TestAccountViews(TestAccountSetUp):

    def test_1_register_new_user(self):
        response = self.client.post(self.register_url, self.user_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(set(response.data), {'id', 'username', 'email'})
        self.assertEqual(response.data.get("username"), self.user_data.get("username"))

    def test_2_error_on_invalid_login_credentials(self):
        login_data = self.login_data.copy()
        login_data["password"] = "invalid_password"
        response = self.client.post(self.login_url, login_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotEqual(set(response.data), {"access", "refresh"})

    def test_3_user_login(self):
        response = self.client.post(self.login_url, self.login_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(set(response.data), {"access", "refresh"})

    def test_4_token_refresh(self):
        response = self.client.post(self.refresh_url, {"refresh": self.refresh_token})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(set(response.data), {"access"})

    def test_5_token_verify(self):
        response = self.client.post(self.verify_url, {"token": self.access_token})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {})

    def test_6_read_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+ self.access_token)
        response = self.client.get(self.profile_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(set(response.data), {'id', 'username', 'email'})

    def test_7_update_profile(self):
        data = {"username": "JohnUpdate"}
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+ self.access_token)
        response = self.client.patch(self.profile_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(set(response.data), {'id', 'username', 'email'})
        self.assertEqual(response.data.get("username"), 'JohnUpdate')

    def test_8_destroy_profile(self):

        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+ self.access_token)
        response = self.client.delete(self.profile_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(email=self.user_data["email"]).exists())