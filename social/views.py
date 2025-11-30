from rest_framework import generics, permissions, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Follow, Post, Comment, Like, CommentLike
from .serializers import (
    FollowSerializer, UserSerializer, SimpleUserSerializer,
    PostSerializer, CommentSerializer
)
from .forms import PostForm, CommentForm
from django.http import JsonResponse


# ---------------------------
# API ENDPOINTS (DRF)
# ---------------------------

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


class FeedView(APIView):
    """Feed via API (JSON)"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        following_users = request.user.following.all().values_list("following", flat=True)
        posts = Post.objects.filter(author__in=following_users).order_by("-created_at")
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


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

    @action(detail=True, methods=["post", "delete"])
    def like(self, request, pk=None):
        post = self.get_object()
        like = Like.objects.filter(user=request.user, post=post)
        if request.method == "POST" and not like.exists():
            Like.objects.create(user=request.user, post=post)
        elif request.method == "DELETE" and like.exists():
            like.delete()
        return Response({"likes_count": post.likes.count()})


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = None
    
    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs["post_pk"]).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post_id=self.kwargs["post_pk"])


# ---------------------------
# VIEWS HTML (Templates)
# ---------------------------

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Post, Follow

@login_required
def feed(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("feed")
    else:
        form = PostForm()

    following_users = Follow.objects.filter(follower=request.user).values_list("following", flat=True)
    posts = Post.objects.filter(author__in=following_users).order_by("-created_at")
    liked_posts = Like.objects.filter(user=request.user).values_list("post_id", flat=True)

    return render(request, "feed.html", {
        "posts": posts,
        "form": form,
        "liked_posts": liked_posts,
    })

from django.utils.timezone import localtime
from django.http import JsonResponse


@login_required
def toggle_follow(request, user_id):
    target_user = get_object_or_404(User, id=user_id)

    if target_user == request.user:
        # não pode seguir a si mesmo, redireciona para o próprio perfil
        return redirect("profile", username=request.user.username)

    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        following=target_user
    )

    if not created:
        # já seguia → desfaz
        follow.delete()

    # redireciona para o perfil do usuário alvo
    return redirect("profile", username=target_user.username)


#Curtir e descurtir um post
@login_required
def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like = Like.objects.filter(user=request.user, post=post)

    if like.exists():
        like.delete()
        liked = False
    else:
        Like.objects.create(user=request.user, post=post)
        liked = True

    return JsonResponse({
        "likes_count": post.likes.count(),
        "liked": liked
    })


# lista com os IDs dos posts que o usuário já curtiu
@login_required
def feed_view(request):
    posts = Post.objects.all().order_by("-created_at")
    liked_posts = Like.objects.filter(user=request.user).values_list("post_id", flat=True)

    return render(request, "feed.html", {
        "posts": posts,
        "liked_posts": liked_posts,
    })

#ver meus posts e criar posts
@login_required
def my_posts_view(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("my-posts")
    else:
        form = PostForm()

    posts = Post.objects.filter(author=request.user).order_by("-created_at")
    liked_posts = Like.objects.filter(user=request.user).values_list("post_id", flat=True)

    return render(request, "feed.html", {
        "posts": posts,
        "form": form,
        "liked_posts": liked_posts,
    })

@login_required
def comments_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            novo_comentario = form.save(commit=False)
            novo_comentario.post = post
            novo_comentario.author = request.user
            novo_comentario.save()
            return JsonResponse({
                "id": novo_comentario.id,
                "author": request.user.username,
                "content": novo_comentario.content,
                "created_at": localtime(novo_comentario.created_at).strftime("%d/%m/%Y %H:%M"),
                "total_comments": post.comments.count(),  # 🔹 contador atualizado
            })
    else:
        comments = Comment.objects.filter(post=post).order_by("-created_at")
        form = CommentForm()
        liked_comments = CommentLike.objects.filter(user=request.user).values_list("comment_id", flat=True)

        return render(request, "comments.html", {
            "post": post,
            "comments": comments,
            "form": form,
            "liked_comments": liked_comments,
        })




# Curtir/descurtir comentário
@login_required
def toggle_comment_like(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    like = CommentLike.objects.filter(user=request.user, comment=comment)

    if like.exists():
        like.delete()
        liked = False
    else:
        CommentLike.objects.create(user=request.user, comment=comment)
        liked = True

    return JsonResponse({
        "likes_count": comment.likes.count(),
        "liked": liked
    })