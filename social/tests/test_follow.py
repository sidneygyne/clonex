from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from social.models import Follow

User = get_user_model()

class FollowToggleAPITest(APITestCase):
    def setUp(self):
        self.user_a = User.objects.create_user(username="user_a", password="123")
        self.user_b = User.objects.create_user(username="user_b", password="123")

        # autenticar user_a via JWT
        response = self.client.post("/api/token/", {"username": "user_a", "password": "123"})
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_follow_user(self):
        """User A deve conseguir seguir User B."""
        response = self.client.post(f"/api/social/follow/{self.user_b.id}/")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Follow.objects.filter(follower=self.user_a, following=self.user_b).exists())

    def test_unfollow_user(self):
        """User A deve conseguir deixar de seguir User B."""
        # primeiro segue
        self.client.post(f"/api/social/follow/{self.user_b.id}/")
        # depois desfaz
        response = self.client.post(f"/api/social/follow/{self.user_b.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Follow.objects.filter(follower=self.user_a, following=self.user_b).exists())

    def test_cannot_follow_self(self):
        """User A não pode seguir a si mesmo."""
        response = self.client.post(f"/api/social/follow/{self.user_a.id}/")
        self.assertEqual(response.status_code, 400)
        self.assertIn("não pode seguir a si mesmo", response.data["detail"])

    def test_followers_list(self):
        """Listar seguidores de user_b"""
        # user_a segue user_b
        Follow.objects.create(follower=self.user_a, following=self.user_b)
        response = self.client.get(f"/api/social/{self.user_b.id}/followers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["username"], "user_a")

    def test_following_list(self):
        """Listar quem user_a está seguindo"""
        Follow.objects.create(follower=self.user_a, following=self.user_b)
        response = self.client.get(f"/api/social/{self.user_a.id}/following/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["username"], "user_b")
