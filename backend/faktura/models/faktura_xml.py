import os

from django.db import models
from django.utils.timezone import now


def faktura_file_path(instance, file):
    return "fakturaer/xml/{}.xlsx".format(now().strftime("%Y%m%d%H%M%S"))

class FakturaXml(models.Model):
    file = models.FileField(upload_to=faktura_file_path)
    created = models.DateTimeField(default=now)

    objects = models.Manager()