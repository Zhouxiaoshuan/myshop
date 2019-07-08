from django import forms

from django.contrib.auth.models import User

class UserLoginForms(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
