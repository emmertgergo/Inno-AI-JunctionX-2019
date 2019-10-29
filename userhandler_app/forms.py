
from django import forms
from django.core import validators
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
                'username': forms.TextInput(attrs={'placeholder': 'username', 'class': 'form-control'}),
                    }
        labels = {
            'username': "Username",
            'password': "Password",
                }


