from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from social.models import Follow, Post

User = get_user_model()

class FeedAPITest(APITestCase):
    def setUp(self):
        # Criando usuários
        self.user_a = User.objects.create_user(username="user_a", password="123")
        self.user_b = User.objects.create_user(username="user_b", password="123")
        self.user_c = User.objects.create_user(username="user_c", password="123")

        # Criando post do user_b
        self.post_b = Post.objects.create(author=self.user_b, content="Post do user_b")

        # user_a segue user_b
        Follow.objects.create(follower=self.user_a, following=self.user_b)

    def authenticate(self, username, password):
        """Helper para obter token JWT e configurar o client."""
        response = self.client.post("/api/token/", {"username": username, "password": password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # garante que o token foi gerado
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_feed_user_a(self):
        """User A deve ver posts de quem segue (user_b)."""
        self.authenticate("user_a", "123")
        response = self.client.get("/api/social/feed/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["content"], "Post do user_b")

    def test_feed_user_c(self):
        """User C não segue user_b, então não deve ver o post."""
        self.authenticate("user_c", "123")
        response = self.client.get("/api/social/feed/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
