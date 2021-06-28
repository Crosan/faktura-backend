import os

from django.db import models
from django.utils.timezone import now
from model_utils import Choices

from ..extra.typechoices import TypeChoices

class Betalergruppe(models.Model):
    navn = models.CharField(max_length=100)
    bgtype = models.CharField(max_length=100, null=True, blank=True, choices=TypeChoices)
    oprettet = models.DateTimeField(default=now)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "%s (%s)" % (self.navn, self.bgtype)
