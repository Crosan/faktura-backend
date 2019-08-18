import os

from django.db import models
from django.utils.timezone import now


def upload_parsing_to(instance, file):
    return "parsed/{} - {}.xlsx".format(instance.data_fil, now().strftime("%Y%m%d%H%M%S"))
    

        
class Parsing(models.Model):
    data_fil = models.FileField(upload_to=upload_parsing_to)
    mangel_liste_fil = models.FileField(blank=True, null=True)
    oprettet = models.DateTimeField(default=now)
    #oprettet_af = models.ForeignKey(
    #    'Profile', related_name='parsings', on_delete=models.PROTECT)
    
    objects = models.Manager()
