from dataclasses import fields
from pyexpat import model
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUp(UserCreationForm):
    email = forms.EmailField(max_length=224, help_text="Required, Inform a valid email Address")

    class Meta:
        model = User
        fields = ('username','email','password1','password2',)