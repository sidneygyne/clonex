from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from accounts.serializers import PasswordChangeSerializer

class PasswordChangeSerializerTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("alice", password="123456")

    def test_invalid_old_password(self):
        serializer = PasswordChangeSerializer(
            data={"old_password": "wrong", "new_password": "newpass"},
            context={"request": type("obj", (), {"user": self.user})()}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
