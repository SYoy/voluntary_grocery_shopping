from django import forms
from django.contrib.auth.models import User

from .choices import STATUS_CHOICES
from EinkaufsApp.models import Einkaufsauftrag


class EinkaufsauftragForm(forms.ModelForm):
    nachricht = forms.CharField(widget=forms.Textarea(attrs={"rows": 4, "cols": 80}), required=True,
                                help_text='Nachricht an die Helfer:',
                                initial='Schreiben Sie eine kurze Nachricht an die HelferInnen, wie Ihnen geholfen werden kann.\n'
                                        'Bitte nennen Sie nicht Ihren Namen oder andere private Information, '+
                                        'damit Ihre Anfrage anonym behandelt werden kann'+
                                        'Wenn Sie einen Lebensmitteleinkauf, Apothekenabholung oder Transport/Fahrt benötigen,'
                                        'schreiben Sie das hier')

    liste_text = forms.CharField(widget=forms.Textarea(attrs={"rows": 10,
                                                              "cols": 80
                                                              }), required=True,
                                help_text="Einkaufsliste/Auftrag hier genauer angeben:",
                                 initial='Beispielsweise: \nEinkauf: Eier, Milch, Mehl, Bananen\n'+
                                         'oder\nTransport zum Arzt: von .. nach ..')

    telefonnummer = forms.CharField(widget=forms.Textarea(attrs={"rows": 1, "cols": 25}), required=True,
                                help_text="Telefonnummer hier eintragen. Ihre Nummer wird nur an die HelferIn übermittelt, die ihren Einkauf/Auftag tätigen wird.")

    budget = forms.CharField(max_length=4, widget=forms.Textarea(attrs={"rows": 1, "cols": 6}), required=True,
                             help_text="Falls für Sie eingekauft wird: Wiel Geld darf Ihr Einkauf maximal kosten? (Angabe in €)",
                             initial="0")

    class Meta:
        model = Einkaufsauftrag
        fields = ("nachricht", "liste_text", "telefonnummer", "budget")