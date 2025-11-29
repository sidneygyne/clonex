from django import forms
from .models import Profile 

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
