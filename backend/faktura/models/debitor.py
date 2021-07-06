import os

from django.db import models
from django.db.models.enums import Choices
from django.utils.timezone import now

regioner = Choices(('Hovedstaden', 'Hovedstaden'),
                   ('Sjælland', 'Sjælland'),
                   ('Syddanmark', 'Syddanmark'),
                   ('Midtjylland', 'Midtjylland'),
                   ('Nordjylland', 'Nordjylland'))

class Debitor(models.Model):
    debitor_nr = models.CharField(max_length=100, null=True)
    gruppe = models.CharField(max_length=100, null=True)
    navn = models.CharField(max_length=100, null=True)
    GLN_nummer = models.CharField(max_length=100, null=True)
    region = models.CharField(max_length=100, null=True, blank=True, choices=regioner)

    def __str__(self):
        return "%d - %s" % (self.id, self.navn)

    # objects = models.Manager()