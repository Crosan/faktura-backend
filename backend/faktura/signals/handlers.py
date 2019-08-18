from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from backend.faktura.models import *

from backend.faktura.extra.parser import Parser
    
@receiver(post_save, sender=Faktura)
def faktura_created(sender, **kwargs):
    instance = kwargs['instance']
    
    status = FakturaStatus.objects.create(status=10, faktura=instance)
    
@receiver(post_save, sender=FakturaStatus)
def faktura_status_created(sender, **kwargs):
    instance = kwargs['instance']
    
    instance.faktura.status = instance.status


