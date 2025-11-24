from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()

class PostAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="author", password="123")
        # Obter token JWT
        response = self.client.post("/api/token/", {"username": "author", "password": "123"})
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_create_post(self):
        response = self.client.post("/api/social/posts/", {"content": "Meu primeiro post"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["content"], "Meu primeiro post")
