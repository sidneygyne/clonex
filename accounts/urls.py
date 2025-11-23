from django.urls import path
from .views import RegisterView, MeProfileView, PasswordChangeView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("me/", MeProfileView.as_view(), name="me-profile"),
    path("me/password/", PasswordChangeView.as_view(), name="change-password"),
]
