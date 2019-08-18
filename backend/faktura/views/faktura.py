from rest_framework import viewsets

from backend.faktura.models import Faktura
from backend.faktura.serializers import FakturaSerializer, NestedFakturaSerializer


class FakturaViewSet(viewsets.ModelViewSet):
    queryset = Faktura.objects.all()
    serializer_class = FakturaSerializer
    
class NestedFakturaViewSet(viewsets.ModelViewSet):
    queryset = Faktura.objects.all()
    serializer_class = NestedFakturaSerializer
