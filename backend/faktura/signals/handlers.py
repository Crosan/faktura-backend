from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from backend.faktura.models import ReceiptFile

from backend.faktura.extra.receipt_file_parser import Parser


@receiver(post_save, sender=ReceiptFile)
def receipt_file_created(sender, **kwargs):
    instance = kwargs['instance']

    Parser.parse(instance.file)


