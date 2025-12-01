from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView, LoginView as DjangoLoginView
from django.urls import reverse

from .models import Profile
from .serializers import (
    RegisterSerializer, ProfileSerializer,
    ProfileUpdateSerializer, PasswordChangeSerializer
)
from .forms import ProfileForm
from social.models import Follow
from social.models import Post
from .forms import CustomUserCreationForm


# ---------------------------
# PERFIL HTML
# ---------------------------
@login_required
def profile_view(request, username=None):
    user_obj = get_object_or_404(User, username=username)
    profile = user_obj.profile

    is_following = Follow.objects.filter(
        follower=request.user,
        following=user_obj
    ).exists()

    followers = User.objects.filter(following__following=user_obj)
    following = User.objects.filter(followers__follower=user_obj)

    # ✅ buscar posts do usuário
    posts = Post.objects.filter(author=user_obj).order_by("-created_at")

    if request.user == user_obj:
        if request.method == "POST":
            form = ProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                return redirect("profile", username=request.user.username)
        else:
            form = ProfileForm(instance=profile)
    else:
        form = None

    return render(request, "profile.html", {
        "profile": profile,
        "form": form,
        "is_following": is_following,
        "followers": followers,
        "following": following,
        "posts": posts,   # ✅ enviar posts para o template
    })


# ---------------------------
# API VIEWS
# ---------------------------
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

    def put(self, request, *args, **kwargs):
        serializer = ProfileUpdateSerializer(
            request.user.profile, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(ProfileSerializer(request.user.profile).data)


class PasswordChangeView(generics.GenericAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Senha alterada com sucesso."})

class CustomLoginView(DjangoLoginView):
    template_name = "login.html"

    def get_success_url(self):
        # Redireciona para o perfil do usuário logado
        return reverse("profile", kwargs={"username": self.request.user.username})
        return reverse("profile", kwargs={"username": self.request.user.username})


# ---------------------------
# REGISTER HTML
# ---------------------------
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return render(request, "register.html", {
                "form": CustomUserCreationForm(),
                "show_modal": True,
                "username": user.username
            })
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})
