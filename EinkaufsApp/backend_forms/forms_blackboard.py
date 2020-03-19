from django import forms
from django.db import models

from .choices import STATUS_CHOICES, LOCATION_CHOICES


class SelectionForm(forms.Form):
    location = forms.ChoiceField(choices=LOCATION_CHOICES)
    status = forms.ChoiceField(choices=STATUS_CHOICES)

    objects = models.Manager()

    def __init__(self, *args, **kwargs):
        super(SelectionForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                # 'class': 'form-control',
                'id': name
            })
