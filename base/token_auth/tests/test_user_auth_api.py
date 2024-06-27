from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from address.models import UserAddress


User = get_user_model()

print("Loading test_user_api.py")

class UserApiTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="test_user", phone="+79999999999",
                                        password="testing123321", first_name="Test", last_name="User",
                                        email="testuser@gmail.com")
        self.user_2 = User.objects.create_user(username="test_user_2", phone="+77777777777",
                                        password="testing123321", first_name="Test_2", last_name="User",
                                        email="testuser2@gmail.com")
        
    def login(self):
        url = reverse("auth:login")
        
        login_data = {
            "phone": self.user.phone,
            "password": "testing123321"
        }
        
        response = self.client.post(url, data=login_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_register(self):
        url = reverse("auth:register")
        
        register_data = {
            "username": "test_user_3",
            "email": "testuser3@gmail.com",
            "first_name": "Test",
            "last_name": "User",
            "phone": "+79499999999",
            "password": "testing123321"
        }
        
        response = self.client.post(url, data=register_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        test_user_3 = User.objects.filter(phone=register_data["phone"]).first()
        
        self.assertTrue(test_user_3)
        self.assertEqual(test_user_3.username, register_data["username"])
        self.assertEqual(test_user_3.email, register_data["email"])
        
        
    def test_user_login(self):
        # Login
        self.login()
        
        # Проверка наличия access и refresh токенов у пользователя
        self.assertIn("access_token", self.client.cookies.keys())
        self.assertIn("refresh_token", self.client.cookies.keys())
        
        # Проверка, что access и refresh токены не пустые
        self.assertTrue(self.client.cookies["access_token"].value)
        self.assertTrue(self.client.cookies["refresh_token"].value)
        
    
    def test_user_logout(self):
        # Login
        self.login()
        # Проверка наличия access и refresh токенов у пользователя
        self.assertIn("access_token", self.client.cookies.keys())
        self.assertIn("refresh_token", self.client.cookies.keys())
        
        # Проверка, что access и refresh токены не пустые
        self.assertTrue(self.client.cookies["access_token"].value)
        self.assertTrue(self.client.cookies["refresh_token"].value)
        
        # Logout
        logout_url = reverse("auth:logout")
        
        response = self.client.post(logout_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Проверка, что запрос, требующий аутентификации, возвращает ошибку
        protected_url = reverse("auth:user-detail", kwargs={"username": self.user.username})
        response = self.client.get(protected_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
         
        
    def test_user_detail_get(self):
        # Login
        self.login()
        
        # User detail success
        success_user_detail_url = reverse("auth:user-detail", kwargs={"username": self.user.username})

        response = self.client.get(success_user_detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # User detail error
        error_user_detail_url = reverse("auth:user-detail", kwargs={"username": self.user_2.username})
        
        response = self.client.get(error_user_detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        
    def test_user_detail_put(self):
        # Login
        self.login()
        
        # User detail put
        user_detail_url = reverse("auth:user-detail", kwargs={"username": self.user.username})
        
        user_data = {
            "id": self.user.id,
            "username": "new_test_user_username",
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "email": self.user.email,
            "phone": str(self.user.phone),
            "address": ""
        }
        response = self.client.get(user_detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.put(user_detail_url, data=user_data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, user_data["username"])
        
        