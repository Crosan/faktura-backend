from django.db import models

class Region(models.Model):
    navn = models.CharField(max_length=50)

    def __str__(self):
        return self.navn