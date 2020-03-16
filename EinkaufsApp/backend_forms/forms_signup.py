from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

LOCATION_CHOICES = (
    ('MBG','Malschenberg'),
    ('RBG','Rauenberg'),
    ('ROTBG','Rotenberg'),
)

class SignUpForm(UserCreationForm):
    vorname = forms.CharField(max_length=30, required=True, help_text='Bitte ausfüllen. Ihr Name und ihre Email wird nicht veröffentlicht. ')
    nachname = forms.CharField(max_length=30, required=True, help_text='Bitte ausfüllen. Ihr Name und ihre Email wird nicht veröffentlicht.')
    email = forms.EmailField(max_length=254, required=True, help_text='Bitte eine gültige Email-Adresse eingeben. Ihr Name und ihre Email wird nicht veröffentlicht.')
    location = forms.ChoiceField(choices=LOCATION_CHOICES)

    class Meta:
        model = User
        fields = ('username', 'vorname', 'nachname', 'email', 'location', 'password1', 'password2', )

class SignUpFormHelper(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Bitte ausfüllen.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Bitte ausfüllen.')
    email = forms.EmailField(max_length=254, help_text='Bitte eine gültige Email-Adresse eingeben.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class SignUpFormInNeed(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Bitte ausfüllen.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Bitte ausfüllen.')
    email = forms.EmailField(max_length=254, help_text='Bitte eine gültige Email-Adresse eingeben.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

