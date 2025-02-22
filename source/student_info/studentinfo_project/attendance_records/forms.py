
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    username=forms.CharField(label='Username',max_length=20,required=True)
    password=forms.CharField(label='Password',min_length=8,max_length=20,required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username,password=password)

            if user is None:
                raise forms.ValidationError("Invalid Username and Password")