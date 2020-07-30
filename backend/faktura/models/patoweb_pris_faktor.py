import os

from django.db import models
from django.utils.timezone import now

class PatowebPrisFaktor(models.Model):
    RgH = models.FloatField(default=0)
    praksis = models.FloatField(default=0)
    grønland = models.FloatField(default=0)
    andet = models.FloatField(default=0)
    gyldig_fra = models.DateTimeField(default=now)
    gyldig_til = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-gyldig_fra']