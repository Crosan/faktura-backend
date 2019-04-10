import os

from django.db import models
from django.utils.timezone import now

class AnalyseType(models.Model):
    ydelses_kode = models.CharField(max_length=50)
    ydelses_navn = models.CharField(max_length=100)
    gruppering = models.CharField(max_length=100)
    type = models.CharField(max_length=100, blank=True, null=True)
    kilde_navn = models.CharField(max_length=100, blank=True, null=True)
    gyldig_fra = models.DateTimeField(default=now)
    gyldig_til = models.DateTimeField(blank=True, null=True)    

    objects = models.Manager()