from rest_framework import viewsets

from backend.faktura.models import ParsingStatus
from backend.faktura.serializers import ParsingStatusSerializer


class ParsingStatusViewSet(viewsets.ModelViewSet):
    queryset = ParsingStatus.objects.all()
    serializer_class = ParsingStatusSerializer
