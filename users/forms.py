from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 'password1',
            'password2'
        ]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(required=False, max_length=20)
    last_name = forms.CharField(required=False, max_length=20)
    bio = forms.CharField(required=False,
                          max_length=5000,
                          widget=forms.Textarea(),
                          help_text='Write your bio here!')

    class Meta:
        model = Profile
        fields = ['image', 'first_name', 'last_name', 'bio']
