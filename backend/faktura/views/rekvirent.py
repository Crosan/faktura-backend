from rest_framework import viewsets

from backend.faktura.models import Rekvirent
from backend.faktura.serializers import RekvirentSerializer, NestedRekvirentSerializer


class RekvirentViewSet(viewsets.ModelViewSet):
    queryset = Rekvirent.objects.all()
    serializer_class = RekvirentSerializer
    
class NestedRekvirentViewSet(viewsets.ModelViewSet):
    queryset = Rekvirent.objects.all()
    serializer_class = NestedRekvirentSerializer
