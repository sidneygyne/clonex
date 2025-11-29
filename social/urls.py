from django.urls import path, include
from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter
from .views import (
    PostViewSet, FollowToggleView, FollowersListView, FollowingListView,
    FeedView, CommentViewSet, feed, comments_view
)
from .views import toggle_follow
from .views import toggle_like

# API routers
router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")

posts_router = routers.NestedDefaultRouter(router, "posts", lookup="post")
posts_router.register("comments", CommentViewSet, basename="post-comments")

urlpatterns = [
    # API endpoints
    path("follow/<int:user_id>/", FollowToggleView.as_view(), name="follow-toggle"),
    path("<int:user_id>/followers/", FollowersListView.as_view(), name="followers-list"),
    path("<int:user_id>/following/", FollowingListView.as_view(), name="following-list"),
    path("feed/api/", FeedView.as_view(), name="feed-api"),  # API JSON
    path("", include(router.urls)),
    path("", include(posts_router.urls)),

    # HTML views
    path("feed/", feed, name="feed"),  # HTML template
    path("post/<int:post_id>/comments/", comments_view, name="comments"),

    path("follow/html/<int:user_id>/", toggle_follow, name="toggle-follow"),

    path("like/<int:post_id>/", toggle_like, name="toggle-like"),
    
]
