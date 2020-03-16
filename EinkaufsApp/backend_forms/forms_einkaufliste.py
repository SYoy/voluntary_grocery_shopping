from django import forms
from django.contrib.auth.models import User
from EinkaufsApp.models import Einkauf

STATUS_CHOICES = (
    ("aktiv", "akt"),
    ("angenommen", "ang"),
    ("default", "def"),
    ("abgeschlossen", "abg")
)

class Einkaufsauftrag(forms.Form):
    nachricht = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 80}),
                                help_text='Nachricht an die Helfer, bitte nicht Ihren Namen oder andere private Information nennen.')

    liste_text = forms.CharField(widget=forms.Textarea(attrs={"rows": 20, "cols": 80}),
                                help_text="Einkaufsliste hier eintragen")

    telefonnummer = forms.CharField(widget=forms.Textarea(attrs={"rows": 1, "cols": 25}),
                                help_text="Telefonnummer hier eintragen. Ihre Nummer wird nur an die HelferIn übermittelt, die ihren Einkauf tätigen möchte.")

    budget = forms.CharField(max_length=4, widget=forms.Textarea(attrs={"rows": 1, "cols": 5}),
                             help_text="Wie viel Geld darf Ihr Einkauf maximal kosten?")
    # status = forms.CharField(max_length=13, choices=STATUS_CHOICES, default='default')

    # auftragsdatum = forms.DateTimeField()
    # abschlussdatum = forms.DateTimeField()