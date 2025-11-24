from rest_framework import generics, permissions, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Follow, Post, Comment, Like
from .serializers import FollowSerializer, UserSerializer, SimpleUserSerializer, PostSerializer, CommentSerializer


# Endpoints de seguir/deixar de seguir
class FollowToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        """Seguir ou deixar de seguir um usuário."""
        target_user = get_object_or_404(User, id=user_id)

        if target_user == request.user:
            return Response({"detail": "Você não pode seguir a si mesmo."}, status=400)

        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=target_user
        )

        if not created:
            # já existe → desfaz o follow
            follow.delete()
            return Response({"detail": "Unfollow realizado com sucesso."}, status=200)

        serializer = FollowSerializer(follow)
        return Response(serializer.data, status=201)


class FollowersListView(generics.ListAPIView):
    serializer_class = SimpleUserSerializer
    pagination_class = None  

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return User.objects.filter(
            id__in=Follow.objects.filter(following_id=user_id)
                                 .values_list("follower_id", flat=True)
        ).order_by("id")

class FollowingListView(generics.ListAPIView):
    serializer_class = SimpleUserSerializer
    pagination_class = None 

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return User.objects.filter(
            id__in=Follow.objects.filter(follower_id=user_id)
                                 .values_list("following_id", flat=True)
        ).order_by("id")


# Endpoint de Feed
class FeedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        following_users = request.user.following.all().values_list("following", flat=True)
        posts = Post.objects.filter(author__in=following_users).order_by("-created_at")
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


# CRUD de Postagens
class IsOwnerOrReadOnly(permissions.BasePermission):
    """Permite edição apenas ao autor do post"""
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # Curtidas (Likes)
    @action(detail=True, methods=["post", "delete"])
    def like(self, request, pk=None):
        post = self.get_object()
        like = Like.objects.filter(user=request.user, post=post)
        if request.method == "POST" and not like.exists():
            Like.objects.create(user=request.user, post=post)
        elif request.method == "DELETE" and like.exists():
            like.delete()
        return Response({"likes_count": post.likes.count()})


# Commentários
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = None
    
    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs["post_pk"]).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post_id=self.kwargs["post_pk"])


