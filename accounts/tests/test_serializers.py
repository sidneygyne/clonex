from accounts.serializers import RegisterSerializer
from django.contrib.auth.models import User
from django.test import TestCase
from accounts.serializers import PasswordChangeSerializer

class PasswordChangeSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("bob", password="123456")

    def test_invalid_old_password(self):
        serializer = PasswordChangeSerializer(
            data={"old_password": "wrong", "new_password": "newpass"},
            context={"request": type("obj", (), {"user": self.user})()}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_valid_password_change(self):
        serializer = PasswordChangeSerializer(
            data={"old_password": "123456", "new_password": "newpass"},
            context={"request": type("obj", (), {"user": self.user})()}
        )
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertTrue(user.check_password("newpass"))

    def test_invalid_email(self):
        data = {"username": "bob", "email": "not-an-email", "password": "123456"}
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)