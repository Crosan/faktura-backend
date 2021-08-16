import os
from backend.faktura.models.region import Region


from django.db import models
from model_utils import Choices
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
    adresse = models.CharField(max_length=256, null=True)
    region = models.CharField(max_length=100, null=True, choices=regioner)
    # region = models.ForeignKey(Region, related_name="debitorer", null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "%d - %s" % (self.id, self.navn)

    # objects = models.Manager()