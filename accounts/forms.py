from django import forms
from .models import Profile 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar", "display_name", "bio"]
        labels = {
            "avatar": "Foto de Perfil",
            "display_name": "Nome",
            "bio": "Bio",
        }
        widgets = {
            "display_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Seu nome"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Fale sobre você"}),
            "avatar": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove o help_text do campo username
        self.fields["username"].help_text = None
        # Opcional: remover help_text dos campos de senha também
        self.fields["password1"].help_text = None
        self.fields["password2"].help_text = None
        # Adicionar classes Bootstrap
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"