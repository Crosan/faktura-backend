import os

from django.db import models
from django.utils.timezone import now

from model_utils import Choices

FakturaStatusChoices = Choices((10, 'oprettet'), (20, 'faktura sendt'), (30, 'slettet'))


def upload_faktura_to(instance, file):
    return "fakturaer/{} - {}.pdf".format(instance.id, now().strftime("%Y%m%d%H%M%S"))
    
class FakturaStatus(models.Model):
    oprettet = 10
    faktura = 20
    slettet = 30

    status = models.IntegerField(choices=FakturaStatusChoices)
    dato = models.DateTimeField(default=now)
    faktura = models.ForeignKey(
        'Faktura', related_name="status_historik", on_delete=models.CASCADE)
    #oprettet_af = models.ForeignKey(
    #    'Profile', related_name='parsings', on_delete=models.PROTECT)
        
    objects = models.Manager()
    
        
class Faktura(models.Model):
    pdf_fil = models.FileField(upload_to=upload_faktura_to, null=True, blank=True)
    oprettet = models.DateTimeField(default=now)
    antal_linjer = models.IntegerField(default=0)
    samlet_pris = models.FloatField(default=0)
    status = models.IntegerField(default=10, choices=FakturaStatusChoices)
    parsing = models.ForeignKey(
        'Parsing', related_name="fakturaer", on_delete=models.CASCADE)    
    rekvirent = models.ForeignKey(
        'Rekvirent', related_name='fakturaer', on_delete=models.PROTECT, blank=True, null=True)
    
    objects = models.Manager()

    def __str__(self):
        return "%d - %s" % (self.id, self.rekvirent.afdelingsnavn)
