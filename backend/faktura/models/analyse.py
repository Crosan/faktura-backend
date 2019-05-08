import os

from django.db import models
from django.utils.timezone import now

from .analyse_type import AnalyseType
from .rekvirent import Rekvirent

class Analyse(models.Model):
    antal = models.IntegerField(default=1)
    pris = models.CharField(max_length=50)
    CPR = models.CharField(max_length=50)
    afregnings_dato = models.DateTimeField(default=now)
    svar_dato = models.DateTimeField(blank=True, null=True)
    analyse_type = models.ForeignKey(
        'AnalyseType', related_name='analyser', on_delete=models.PROTECT, blank=True, null=True)
    rekvirent = models.ForeignKey(
        'Rekvirent', related_name='analyser', on_delete=models.PROTECT, blank=True, null=True)
    parsing = models.ForeignKey(
        'Parsing', related_name='analyser', on_delete=models.CASCADE, blank=True, null=True)

    objects = models.Manager()