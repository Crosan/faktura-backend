from rest_framework import viewsets

from backend.faktura.models import ReceiptFile
from backend.faktura.serializers import ReceiptFileSerializer


class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = ReceiptFile.objects.all()
    serializer_class = ReceiptFileSerializer