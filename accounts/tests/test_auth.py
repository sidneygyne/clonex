from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()

class AuthTests(APITestCase):
    def test_register_and_login(self):
        # Cadastro
        res = self.client.post("/api/accounts/register/", {
            "username": "sidney",
            "email": "sidney@example.com",
            "password": "123456"
        })
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Login JWT
        res = self.client.post("/auth/login/", {
            "username": "sidney",
            "password": "123456"
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)

    def test_register_with_invalid_email(self):
        """Cadastro deve falhar com email inválido"""
        res = self.client.post("/api/accounts/register/", {
            "username": "bob",
            "email": "not-an-email",
            "password": "123456"
        })
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", res.data)

    def test_login_wrong_password(self):
        """Login deve falhar com senha incorreta"""
        User.objects.create_user(username="alice", password="123456")
        res = self.client.post("/auth/login/", {
            "username": "alice",
            "password": "wrong"
        })
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_nonexistent_user(self):
        """Login deve falhar com usuário inexistente"""
        res = self.client.post("/auth/login/", {
            "username": "ghost",
            "password": "123456"
        })
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
