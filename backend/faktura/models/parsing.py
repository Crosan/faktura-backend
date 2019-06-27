import os

from django.db import models
from django.utils.timezone import now

from model_utils import Choices

ParsingStatusChoices = Choices((1, 'oprettet'), (2, 'faktura sendt'), (3, 'slettet'))


def upload_parsing_to(instance, file):
    return "parsed/{} - {}.xlsx".format(instance.data_fil, now().strftime("%Y%m%d%H%M%S"))
    
    
class ParsingStatus(models.Model):
    oprettet = 1
    faktura = 2
    slettet = 3

    status = models.IntegerField(choices=ParsingStatusChoices)
    dato = models.DateTimeField(default=now)
    parsing = models.ForeignKey(
        'Parsing', related_name="status_historik", on_delete=models.PROTECT)
        
    objects = models.Manager()

        
class Parsing(models.Model):
    data_fil = models.FileField(upload_to=upload_parsing_to)
    mangel_liste_fil = models.FileField(blank=True, null=True)
    oprettet = models.DateTimeField(default=now)
    antal_oprettet = models.IntegerField(default=1)
    samlet_pris = models.FloatField(default=0)
    #oprettet_af = models.ForeignKey(
    #    'Profile', related_name='parsings', on_delete=models.PROTECT)
    status = models.IntegerField(default=1, choices=ParsingStatusChoices)
    
    objects = models.Manager()
