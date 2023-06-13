from django import forms
from .models import User

class CreateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password', 'full_name', 'bio', 'profile_picture']
