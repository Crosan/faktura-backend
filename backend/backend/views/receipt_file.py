from rest_framework import viewsets

from backend.backend.models import ReceiptFile
from backend.backend.serializers import ReceiptFileSerializer


class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = ReceiptFile.objects.all()
    serializer_class = ReceiptFileSerializer