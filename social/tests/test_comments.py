from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from social.models import Post, Comment

User = get_user_model()

class CommentViewSetTests(APITestCase):
    def setUp(self):
        # cria usuário e autentica
        self.user = User.objects.create_user(username="alice", password="123456")
        res = self.client.post("/auth/login/", {"username": "alice", "password": "123456"})
        token = res.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        # cria post
        self.post = Post.objects.create(author=self.user, content="Post de teste")

    def test_create_comment(self):
        """Usuário deve conseguir criar comentário em um post"""
        url = f"/api/social/posts/{self.post.id}/comments/"
        response = self.client.post(url, {"content": "Comentário de teste"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().content, "Comentário de teste")

    def test_list_comments(self):
        """Usuário deve conseguir listar comentários de um post"""
        Comment.objects.create(author=self.user, post=self.post, content="Primeiro comentário")
        Comment.objects.create(author=self.user, post=self.post, content="Segundo comentário")

        url = f"/api/social/posts/{self.post.id}/comments/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["content"], "Segundo comentário")  # ordenado por -created_at
