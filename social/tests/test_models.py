from django.test import TestCase
from django.contrib.auth import get_user_model
from social.models import Follow, Post, Like, Comment

User = get_user_model()

class FollowModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="123")
        self.user2 = User.objects.create_user(username="user2", password="123")

    def test_follow_unique(self):
        Follow.objects.create(follower=self.user1, following=self.user2)
        with self.assertRaises(Exception):
            Follow.objects.create(follower=self.user1, following=self.user2)

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="author", password="123")

    def test_post_content_length(self):
        post = Post.objects.create(author=self.user, content="a"*280)
        self.assertEqual(len(post.content), 280)
