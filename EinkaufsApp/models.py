from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

LOCATION_CHOICES = (
    ('Malschenberg','MBG'),
    ('Rauenberg', 'RBG'),
    ('Rotenberg','ROTBG'),
)

GROUP_CHOICES = (
    ('Helfer','H'),
    ('Empfaenger', 'E'),
    ('default', 'D')
)

STATUS_CHOICES = (
    ("aktiv", "akt"),
    ("angenommen", "ang"),
    ("default", "def"),
    ("abgeschlossen", "abg")
)

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=12, choices=LOCATION_CHOICES, default='RBG')
    group = models.CharField(max_length=12, choices=GROUP_CHOICES, default='D')

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Person.objects.create(user=instance)
    instance.person.save()

class Einkauf(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nachricht = models.TextField(max_length=200, default="Nachricht an die Helfer")
    liste_text = models.TextField(max_length=500, default="Einkaufsliste hier eintragen")
    telefonnummer = models.TextField(max_length=25, default="06222000000",
                                    help_text="Telefonnummer hier eintragen. Ihre Nummer wird nur an die HelferIn übermittelt, die ihren Einkauf tätigen möchte.")
    budget = models.CharField(max_length=4, default="30")
    auftragsdatum = models.DateTimeField()
    abschlussdatum = models.DateTimeField()
    status = models.CharField(max_length=13, choices=STATUS_CHOICES, default='default')