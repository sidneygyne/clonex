from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, FollowToggleView, FollowersListView, FollowingListView, FeedView

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [
    path("follow/<int:user_id>/", FollowToggleView.as_view(), name="follow-toggle"),
    path("followers/<int:user_id>/", FollowersListView.as_view(), name="followers-list"),
    path("following/<int:user_id>/", FollowingListView.as_view(), name="following-list"),
    path("feed/", FeedView.as_view(), name="feed"),
    path("", include(router.urls)),
]
