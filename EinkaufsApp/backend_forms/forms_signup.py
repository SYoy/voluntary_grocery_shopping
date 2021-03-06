from django import forms
from django.urls import reverse
from django.utils.functional import lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .choices import LOCATION_CHOICES_FORM


class SignUpForm(UserCreationForm):
    firstname = forms.CharField(max_length=30, required=True, help_text='Bitte ausfüllen. Ihr Name und ihre Email wird nicht veröffentlicht. ', label="Vorname")
    lastname = forms.CharField(max_length=30, required=True, help_text='Bitte ausfüllen. Ihr Name und ihre Email wird nicht veröffentlicht.', label="Nachname")
    email = forms.EmailField(max_length=254, required=True, help_text='Bitte eine gültige Email-Adresse eingeben. Ihr Name und ihre Email-Adresse wird nicht veröffentlicht.', label="Email-Adresse")
    location = forms.ChoiceField(choices=LOCATION_CHOICES_FORM, label="Ortsteil")
    datenschutz = forms.BooleanField(required=True, label='Akzeptieren der Datenschutzerklärung')


    class Meta:
        model = User
        fields = ('username', 'firstname', 'lastname', 'email', 'location', 'password1', 'password2', )