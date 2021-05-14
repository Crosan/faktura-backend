import os

from django.db import models
from django.utils.timezone import now

class Debitor(models.Model):
    debitor_nr = models.CharField(max_length=100, null=True)
    gruppe = models.CharField(max_length=100, null=True)
    navn = models.CharField(max_length=100, null=True)
    GLN_nummer = models.CharField(max_length=100, null=True)

    def __str__(self):
        return "%d - %s" % (self.id, self.navn)

    # objects = models.Manager()