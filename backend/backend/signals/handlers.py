from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from backend.backend.models import ReceiptFile

from backend.backend.extra.receipt_file_parser import Parser


@receiver(post_save, sender=ReceiptFile)
def receipt_file_created(sender, **kwargs):
    instance = kwargs['instance']

    Parser.parse(instance.file)


