from django import forms
from .models import Profile  # ajuste o import conforme seu projeto

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar", "display_name", "bio"]
