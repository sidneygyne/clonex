from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Follow
from .serializers import FollowSerializer, UserSerializer
from .models import Post
from .serializers import PostSerializer

# Endpoints de seguir/deixar de seguir
class FollowToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = User.objects.get(id=user_id)
        follow, created = Follow.objects.get_or_create(
            follower=request.user, following=target
        )
        if created:
            return Response({"detail": f"Agora você segue {target.username}"})
        return Response({"detail": f"Você já segue {target.username}"})

    def delete(self, request, user_id):
        target = User.objects.get(id=user_id)
        Follow.objects.filter(follower=request.user, following=target).delete()
        return Response({"detail": f"Você deixou de seguir {target.username}"})

class FollowersListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return User.objects.filter(following__following_id=user_id)

class FollowingListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return User.objects.filter(followers__follower_id=user_id)

# Endpoint de Feed
class FeedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        following_ids = Follow.objects.filter(
            follower=request.user
        ).values_list("following_id", flat=True)
        posts = Post.objects.filter(author_id__in=following_ids).order_by("-created_at")
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)