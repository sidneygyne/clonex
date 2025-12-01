from django.urls import path
from django.contrib.auth.views import LoginView
from .views import RegisterView, MeProfileView, PasswordChangeView, profile_view

urlpatterns = [
    path("register/", RegisterView.as_view(), name="accounts-register"),
    path("login/", LoginView.as_view(), name="accounts-login"),
    path("me/", MeProfileView.as_view(), name="me-profile"),
    path("me/password/", PasswordChangeView.as_view(), name="change-password"),

    # Perfil pelo username
    path("<str:username>/", profile_view, name="profile"),
]

