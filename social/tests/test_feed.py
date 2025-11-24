from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from social.models import Post, Follow

class FeedTests(APITestCase):
    def setUp(self):
        self.u1 = User.objects.create_user("alice", password="123456")
        self.u2 = User.objects.create_user("bob", password="123456")
        self.client.post("/auth/login/", {"username": "alice", "password": "123456"})
        res = self.client.post("/auth/login/", {"username": "alice", "password": "123456"})
        self.token = res.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        Follow.objects.create(follower=self.u1, following=self.u2)
        Post.objects.create(author=self.u2, content="Hello world")

    def test_feed_shows_following_posts(self):
        res = self.client.get("/api/social/feed/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["content"], "Hello world")
    
    def test_feed_empty_when_no_following(self):
        """Feed deve estar vazio quando o usuário não segue ninguém"""
        # cria um novo usuário sem seguir ninguém
        u3 = User.objects.create_user("charlie", password="123456")
        res = self.client.post("/auth/login/", {"username": "charlie", "password": "123456"})
        token = res.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        # chama o feed
        response = self.client.get("/api/social/feed/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

class FeedTest(TestCase):
    def setUp(self):
        # Criando usuários
        self.user_a = User.objects.create_user(username="user_a", password="123")
        self.user_b = User.objects.create_user(username="user_b", password="123")
        self.user_c = User.objects.create_user(username="user_c", password="123")

        # Criando post do user_b
        self.post_b = Post.objects.create(author=self.user_b, content="Post do user_b")

        # user_a segue user_b
        Follow.objects.create(follower=self.user_a, following=self.user_b)

    def test_feed_user_a(self):
        """User A deve ver posts de quem segue (user_b)."""
        followed_users = self.user_a.following.values_list("following", flat=True)
        feed_posts = Post.objects.filter(author__in=followed_users)
        self.assertIn(self.post_b, feed_posts)

    def test_feed_user_c(self):
        """User C não segue user_b, então não deve ver o post."""
        followed_users = self.user_c.following.values_list("following", flat=True)
        feed_posts = Post.objects.filter(author__in=followed_users)
        self.assertNotIn(self.post_b, feed_posts)