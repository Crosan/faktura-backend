import os

from django.db import models
from django.utils.timezone import now


def receipt_file_path(instance, file):
    return "receipts/{}.xlsx".format(now().strftime("%Y%m%d%H%M%S"))

class ReceiptFile(models.Model):
    file = models.FileField(upload_to=receipt_file_path)
    created = models.DateTimeField(default=now)

    objects = models.Manager()