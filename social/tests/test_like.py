from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from social.models import Post

User = get_user_model()

class PostLikeTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="123456")
        # autenticar via JWT
        res = self.client.post("/auth/login/", {"username": "alice", "password": "123456"})
        token = res.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        # cria um post
        self.post = Post.objects.create(author=self.user, content="Post de teste")

    def test_like_post(self):
        """Usuário deve conseguir dar like em um post"""
        url = f"/api/social/posts/{self.post.id}/like/"
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["likes_count"], 1)

    def test_unlike_post(self):
        """Usuário deve conseguir remover o like"""
        url = f"/api/social/posts/{self.post.id}/like/"
        # primeiro dá like
        self.client.post(url)
        # depois remove
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["likes_count"], 0)
