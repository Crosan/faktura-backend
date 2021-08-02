from rest_framework import viewsets
from django.db.models import Q

from backend.faktura.models import Rekvirent
from backend.faktura.serializers import RekvirentSerializer, NestedRekvirentSerializer


class RekvirentViewSet(viewsets.ModelViewSet):
    queryset = Rekvirent.objects.all()
    # queryset = Rekvirent.objects.all().annotate(bg=rekvirenter__betalergruppe__navn)
    serializer_class = RekvirentSerializer
    
class NestedRekvirentViewSet(viewsets.ModelViewSet):
    queryset = Rekvirent.objects.all()
    serializer_class = NestedRekvirentSerializer

class MissingRekvirentViewSet(viewsets.ModelViewSet):
    filt = Q(debitor = None)
    queryset = Rekvirent.objects.filter(filt)
    # queryset = Betalergruppe.objects.all().annotate(sum_total=Sum('rekvirenter__fakturaer__samlet_pris', filter=Q(rekvirenter__fakturaer__parsing__id=pk)))
    serializer_class = NestedRekvirentSerializer