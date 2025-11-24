from django.urls import reverse
from rest_framework.test import APIClient
from django.test import TestCase

class AccountsViewErrorTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_invalid_payload(self):
        url = reverse("accounts-register")
        # payload inválido → faltando username e password
        response = self.client.post(url, {}, format="json")
        self.assertEqual(response.status_code, 400)
