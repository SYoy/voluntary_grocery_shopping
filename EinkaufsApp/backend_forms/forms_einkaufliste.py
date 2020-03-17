from django import forms
from django.contrib.auth.models import User

from .choices import STATUS_CHOICES
from EinkaufsApp.models import Einkaufsauftrag


class EinkaufsauftragForm(forms.ModelForm):
    nachricht = forms.CharField(widget=forms.Textarea(attrs={"rows": 3, "cols": 100}), required=True,
                                help_text='Nachricht an die Helfer. Bitte nicht Ihren Namen oder andere private Information eintragen, damit Ihre Anfrage anonym behandelt werden kann:')

    liste_text = forms.CharField(widget=forms.Textarea(attrs={"rows": 15, "cols": 100}), required=True,
                                help_text="Einkaufsliste hier angeben:")

    telefonnummer = forms.CharField(widget=forms.Textarea(attrs={"rows": 1, "cols": 25}), required=True,
                                help_text="Telefonnummer hier eintragen. Ihre Nummer wird nur an die HelferIn übermittelt, die ihren Einkauf tätigen möchte.")

    budget = forms.CharField(max_length=4, widget=forms.Textarea(attrs={"rows": 1, "cols": 5}), required=True,
                             help_text="Budget, wie viel Geld darf Ihr Einkauf maximal kosten? (Angabe in Euro)")

    class Meta:
        model = Einkaufsauftrag
        fields = ("nachricht", "liste_text", "telefonnummer", "budget")