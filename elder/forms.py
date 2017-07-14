from django import forms
from .models import *


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=10)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = OldPerson
        fields = "__all__"


class ContactOldPerson(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.TextInput()


class QuestionnaireRegistration(forms.Form):
    question = forms.CharField(max_length=1000)
