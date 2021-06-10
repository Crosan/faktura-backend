import os

from django.db import models
from django.utils.timezone import now

class AnalyseType(models.Model):
    ydelses_kode = models.CharField(max_length=50)
    ydelses_navn = models.CharField(max_length=100, blank=True, null=True)
    gruppering = models.CharField(max_length=100, blank=True, null=True)
    afdeling = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    kilde_navn = models.CharField(max_length=100, blank=True, null=True) 

    objects = models.Manager()

    def __str__(self):
        return "%s - %s" % (self.ydelses_navn, self.ydelses_kode)