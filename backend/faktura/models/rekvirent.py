import os

from django.db import models
from django.utils.timezone import now

class Rekvirent(models.Model):
    # hospital = models.CharField(max_length=100)
    niveau = models.CharField(max_length=50, null=True)
    shortname = models.CharField(max_length=100, null=True)
    rekv_nr = models.CharField(max_length=255, null=True)
    GLN_nummer = models.CharField(max_length=100, null=True)
    debitor_nr = models.CharField(max_length=100, null=True)
    betalergruppe = models.ForeignKey(
        'Betalergruppe', related_name='rekvirenter', on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return "%d - %s" % (self.id, self.shortname)

    # objects = models.Manager()