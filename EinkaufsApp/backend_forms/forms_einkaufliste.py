from django import forms
from django.contrib.auth.models import User

from .choices import STATUS_CHOICES
from EinkaufsApp.models import Einkaufsauftrag
from django.core.validators import RegexValidator

class EinkaufsauftragForm(forms.ModelForm):
    tel_regex = RegexValidator(r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$', 'Bitte gültige Telefonnumer angeben!')
    budget_regex = RegexValidator(r'^[0-9]*$', 'Nur Zahlen sind erlaubt')

    nachricht = forms.CharField(widget=forms.Textarea(attrs={"rows": 4, "placeholder": "Schreiben Sie eine kurze Nachricht an die HelferInnen, wie Ihnen geholfen werden kann.\n"+
                                        "Bitte nennen Sie nicht Ihren Namen oder andere private Information."}), required=True,
                                        help_text='Nachricht an die Helfer:')

    liste_text = forms.CharField(widget=forms.Textarea(attrs={"rows": 10, "placeholder":"Einkaufsliste/Auftrag hier genauer angeben. Wenn Sie eine Apothekenabholung oder einen Transport/Fahrt benötigen, schreiben Sie das auch hier"}), required=True,
                                help_text="Einkaufsliste/Auftrag hier genauer angeben. Wenn Sie eine Apothekenabholung oder einen Transport/Fahrt benötigen, schreiben Sie das auch hier")

    telefonnummer = forms.CharField(widget=forms.Textarea(attrs={"rows": 1, "cols": 25, "placeholder":"z.B. 06222-12345"}), required=True, validators=[tel_regex],
                                help_text="Telefonnummer hier eintragen. (Ihre Nummer wird nur an die HelferIn übermittelt, die ihren Einkauf/Auftrag tätigen wird)")

    budget = forms.CharField(max_length=4, widget=forms.Textarea(attrs={"rows": 1, "cols": 6, "placeholder": "0"}), required=True, validators=[budget_regex],
                             help_text="Falls für Sie eingekauft wird: Wie viel Geld darf Ihr Einkauf maximal kosten? (Angabe in €)")

    class Meta:
        model = Einkaufsauftrag
        fields = ("nachricht", "liste_text", "telefonnummer", "budget")