from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile
from rest_framework.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = ("id", "username", "email", "display_name", "avatar", "bio")
        read_only_fields = ["user"]
    
    def validate_avatar(self, value):
        if value.size > 2 * 1024 * 1024:  # 2MB
            raise ValidationError("Imagem muito grande. Limite de 2MB.")
        if not value.name.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            raise ValidationError("Formato inválido. Use JPG, PNG ou WEBP.")
        return value

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("display_name", "avatar", "bio")

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = self.context["request"].user
        if not user.check_password(data["old_password"]):
            raise serializers.ValidationError("Senha atual inválida.")
        return data

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
