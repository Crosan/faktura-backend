from rest_framework import viewsets

from backend.faktura.models import FakturaStatus
from backend.faktura.serializers import FakturaStatusSerializer


class FakturaStatusViewSet(viewsets.ModelViewSet):
    queryset = FakturaStatus.objects.all()
    serializer_class = FakturaStatusSerializer
