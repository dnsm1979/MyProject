from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from users.models import User


class UserLoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ['username', 'password']

    username = forms.CharField()
    password = forms.CharField()



class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "surname",
            "email",
            "password1",
            "password2",
            "position",


        )
    
    first_name = forms.CharField()
    last_name = forms.CharField()
    surname  = forms.CharField()
    username = forms.CharField()
    email = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()
    position  = forms.CharField()



class ProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "surname",
            "position",
            "email",
            "phone_number",)

    first_name = forms.CharField()
    last_name = forms.CharField()
    surname = forms.CharField()
    username = forms.CharField()
    position = forms.CharField()
    email = forms.CharField()
    phone_number = forms.CharField()



