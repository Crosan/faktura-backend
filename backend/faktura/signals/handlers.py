from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from backend.faktura.models import *

from backend.faktura.extra.parser import Parser
    
@receiver(post_save, sender=Parsing)
def parsing_created(sender, **kwargs):
    instance = kwargs['instance']

    Parser.parse(instance)
    
    status = ParsingStatus.objects.create(status=1, parsing=instance)
    
@receiver(post_save, sender=ParsingStatus)
def parsing_status_created(sender, **kwargs):
    instance = kwargs['instance']
    
    instance.parsing.status = instance.status


