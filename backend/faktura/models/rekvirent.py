import os

from django.db import models
from django.utils.timezone import now

class Rekvirent(models.Model):
    hospital = models.CharField(max_length=100)
    niveau = models.CharField(max_length=50)
    afdelingsnavn = models.CharField(max_length=100)
    GLN_nummer = models.CharField(max_length=100)
    betalergruppe = models.ForeignKey(
        'Betalergruppe', related_name='rekvirenter', on_delete=models.PROTECT, blank=True, null=True)

    # objects = models.Manager()