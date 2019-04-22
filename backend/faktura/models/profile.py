import os

from django.db import models
from django.utils.timezone import now

class Profile(models.Model):
    username = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    telephone = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateTimeField(default=now)
    end_date = models.DateTimeField(blank=True, null=True)
    roles = models.TextField(default="[]")

    objects = models.Manager()