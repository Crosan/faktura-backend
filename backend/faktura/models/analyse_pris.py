import os

from django.db import models
from django.utils.timezone import now

from .analyse_type import AnalyseType

class AnalysePris(models.Model):
    intern_pris = models.IntegerField(default=0)
    ekstern_pris = models.IntegerField(default=0)
    gyldig_fra = models.DateTimeField(default=now)
    gyldig_til = models.DateTimeField(blank=True, null=True)
    analyse_type = models.ForeignKey(
        'AnalyseType', related_name='priser', on_delete=models.PROTECT, blank=True, null=True)

    objects = models.Manager()