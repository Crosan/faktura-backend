from rest_framework import viewsets
from django.db.models import Q

from backend.faktura.models import Rekvirent
from backend.faktura.serializers import RekvirentSerializer, NestedRekvirentSerializer


class RekvirentViewSet(viewsets.ModelViewSet):
    queryset = Rekvirent.objects.all()
    # queryset = Rekvirent.objects.all().annotate(bg=rekvirenter__betalergruppe__navn)
    serializer_class = RekvirentSerializer
    
class NestedRekvirentViewSet(viewsets.ModelViewSet):
    # queryset = Rekvirent.objects.all()
    def get_queryset(self):
        searchterm = self.request.query_params.get('q', None)
        if searchterm:
            print(searchterm)
            qs = Rekvirent.objects.filter(Q(debitor__navn__icontains=searchterm) | Q(shortname__icontains=searchterm) | Q(GLN_nummer__icontains=searchterm) | Q(debitor__region__icontains=searchterm) | Q(rekv_nr__icontains=searchterm))
        else:
            qs = Rekvirent.objects.all()
        return qs

    serializer_class = NestedRekvirentSerializer

class MissingRekvirentViewSet(viewsets.ModelViewSet):
    filt = Q(debitor = None)
    queryset = Rekvirent.objects.filter(filt)
    # queryset = Betalergruppe.objects.all().annotate(sum_total=Sum('rekvirenter__fakturaer__samlet_pris', filter=Q(rekvirenter__fakturaer__parsing__id=pk)))
    serializer_class = NestedRekvirentSerializer