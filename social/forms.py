from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content", "image"]  # campos que podem ser editados
        labels = {
            "content": "",
            "image": "",
        }
        widgets = {
            "content": forms.Textarea(attrs={
                "class": "form-control w-100",
                "rows": 4,
                "placeholder": "O que você está pensando?"
            }),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        labels = {
            "content": ""
        }
        widgets = {
            "content": forms.Textarea(attrs={
                "class": "form-control w-100",
                "rows": 2,
                "placeholder": "Escreva um comentário..."
            }),
        }
