from django.urls import path
from .views import FollowToggleView, FollowersListView, FollowingListView

urlpatterns = [
    path("follow/<int:user_id>/", FollowToggleView.as_view(), name="follow-toggle"),
    path("followers/<int:user_id>/", FollowersListView.as_view(), name="followers-list"),
    path("following/<int:user_id>/", FollowingListView.as_view(), name="following-list"),
]
