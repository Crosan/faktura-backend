import os

from django.db import models
from django.utils.timezone import now

class ReceiptRow(models.Model):
    quantity = models.IntegerField()
    key = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    price_internal = models.IntegerField()
    price_internal_kr = models.IntegerField()
    price_external = models.IntegerField(null=True, blank=True)
    price_external_kr = models.IntegerField(null=True, blank=True)
    organisation_key = models.CharField(max_length=100, null=True, blank=True)
    hospital = models.CharField(max_length=100, null=True, blank=True)
    center = models.CharField(max_length=100, null=True, blank=True)
    clinic = models.CharField(max_length=100, null=True, blank=True)

    requestor_key = models.CharField(max_length=100)
    requestor_hospital = models.CharField(max_length=100)

    # These I'm not sure about
    L3Name = models.CharField(max_length=100)
    L4Name = models.CharField(max_length=100)
    L6Org = models.CharField(max_length=100)
    L6Name = models.CharField(max_length=100)


    source_key = models.CharField(max_length=100)
    date = models.DateTimeField()
    date_inserted = models.DateTimeField()

    cpr = models.CharField(max_length=100)
    year = models.CharField(max_length=100)

    import_period = models.CharField(max_length=100)







    objects = models.Manager()