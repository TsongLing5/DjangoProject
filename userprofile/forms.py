from django import forms
# from django.contrib.auth.models import User

# class UserLoginForm(forms.Form):
#     userName=forms.CharField()
#     userPassword=forms.CharField()


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()