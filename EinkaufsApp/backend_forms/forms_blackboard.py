from django import forms
from django.db import models

STATUS_CHOICES = (
    ("AKT", "aktiv"),
    ("ANG", "angenommen"),
    ("DEF", "default"),
    ("ABG", "abgeschlossen")
)

LOCATION_CHOICES = (
    ('ALL', 'Alle Ortsteile'),
    ('MBG', 'Malschenberg'),
    ('RBG', 'Rauenberg'),
    ('ROTBG', 'Rotenberg'),
)


class SelectionForm(forms.Form):
    location = forms.ChoiceField(choices=LOCATION_CHOICES)
    status = forms.ChoiceField(choices=STATUS_CHOICES)

    objects = models.Manager()

    def __init__(self, *args, **kwargs):
        super(SelectionForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
                'id': name
            })
