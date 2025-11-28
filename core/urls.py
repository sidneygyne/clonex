from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import home
from accounts.views import dashboard, register
from social.views import comments_view, feed
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # JWT
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # API
    path("api/accounts/", include("accounts.urls")),
    path("api/social/", include("social.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

    # Front simples (templates)
    path("", home, name="home"),                # página inicial
    path("dashboard/", dashboard, name="dashboard"),  # perfil
    path("feed/", feed, name="feed"),       # feed e comentários HTML

    # Auth templates
    path("accounts/login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("accounts/register/", register, name="register"),

    # Accounts extras
    path("accounts/", include("accounts.urls")),
     path("comments/<int:post_id>/", comments_view, name="comments"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
