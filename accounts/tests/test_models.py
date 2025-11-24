# accounts/tests/test_models.py
from django.test import TestCase
from django.contrib.auth.models import User

class ProfileModelTests(TestCase):
    def test_str_returns_display_name_or_username(self):
        user = User.objects.create_user("alice", password="123456")
        profile = user.profile

        # Sem display_name → deve retornar username
        self.assertEqual(str(profile), "alice")

        # Com display_name → deve retornar display_name
        profile.display_name = "Alice Test"
        profile.save()
        self.assertEqual(str(profile), "Alice Test")
