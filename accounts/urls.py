from django.urls import path
from .views import RegisterView, MeProfileView, PasswordChangeView, LoginView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="accounts-register"),
    path("login/", LoginView.as_view(), name="accounts-login"),
    path("me/", MeProfileView.as_view(), name="me-profile"),
    path("me/password/", PasswordChangeView.as_view(), name="change-password"),
]

