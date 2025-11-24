from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status

class ProfileTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("alice", password="123456")
        res = self.client.post("/auth/login/", {"username": "alice", "password": "123456"})
        self.token = res.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_get_and_update_profile(self):
        res = self.client.get("/api/accounts/me/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["username"], "alice")

        res = self.client.put("/api/accounts/me/", {"display_name": "Alice Test"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["display_name"], "Alice Test")

class ProfileUpdateTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("carol", password="123456")
        res = self.client.post("/auth/login/", {"username": "carol", "password": "123456"})
        self.token = res.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_update_profile_with_empty_data(self):
        res = self.client.put("/api/accounts/me/", {})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Perfil continua válido mesmo sem alterações
        self.assertEqual(res.data["username"], "carol")

    def test_update_profile_with_new_display_name(self):
        res = self.client.put("/api/accounts/me/", {"display_name": "Carol Test"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["display_name"], "Carol Test")
    
    def test_update_profile_with_invalid_field(self):
        res = self.client.put("/api/accounts/me/", {"invalid_field": "x"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotIn("invalid_field", res.data)

    def test_update_profile_with_invalid_payload(self):
        res = self.client.put("/api/accounts/me/", {"display_name": ""})
        assert res.status_code == status.HTTP_400_BAD_REQUEST