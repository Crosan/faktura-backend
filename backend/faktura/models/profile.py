import os

from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    start_dato = models.DateTimeField(default=now)
    slut_dato = models.DateTimeField(blank=True, null=True)
    username = models.CharField(max_length=100, default="NA")
    display_name = models.CharField(max_length=100, default="NA", blank=True, null=True)
    title = models.CharField(max_length=100, default="NA", blank=True, null=True)
    telephone = models.CharField(max_length=100, default="NA", blank=True, null=True)
    email = models.CharField(max_length=100, default="NA", blank=True, null=True)
    er_akademiker = models.BooleanField(default=False)
    er_admin = models.BooleanField(default=False)
    er_bioanalytiker = models.BooleanField(default=False)
    er_bioinformatiker = models.BooleanField(default=False)
    er_sekretaer = models.BooleanField(default=False)
    er_studerende = models.BooleanField(default=False)