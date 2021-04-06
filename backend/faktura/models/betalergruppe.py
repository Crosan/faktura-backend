import os

from django.db import models
from django.utils.timezone import now

class Betalergruppe(models.Model):
    navn = models.CharField(max_length=100)
    bgtype = models.CharField(max_length=100, null=True, blank=True)
    oprettet = models.DateTimeField(default=now)
