from rest_framework import viewsets

from backend.faktura.models import Analyse
from backend.faktura.serializers import AnalyseSerializer, NestedAnalyseSerializer


class AnalyseViewSet(viewsets.ModelViewSet):
    queryset = Analyse.objects.all()
    serializer_class = AnalyseSerializer

    # def get_queryset(self):
    #     parsing = self.request.query_params.get('parsing', None)
    #     rekvirent = self.request.query_params.get('rekvirent', None)
    #     if parsing and rekvirent:
    #         qs = Faktura.objects.filter(parsing__id=parsing, rekvirent__rekvirent__id=rekvirent).order_by('-samlet_pris')
    #     elif parsing:
    #         qs = Faktura.objects.filter(parsing__id=parsing).order_by('-samlet_pris')
    #     else:
    #         qs = Faktura.objects.all()
    #     return qs
    
class NestedAnalyseViewSet(viewsets.ModelViewSet):
    queryset = Analyse.objects.all()
    serializer_class = NestedAnalyseSerializer
