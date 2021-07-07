from rest_framework import viewsets
from django.db.models import Count, Sum

from backend.faktura.models import Faktura
from backend.faktura.serializers import FakturaSerializer, NestedFakturaSerializer, SemiNestedFakturaSerializer


class FakturaViewSet(viewsets.ModelViewSet):
    # queryset = Faktura.objects.all()
    serializer_class = FakturaSerializer

    def get_queryset(self):
        parsing = self.request.query_params.get('parsing', None)
        betalergruppe = self.request.query_params.get('betalergruppe', None)
        debitor = self.request.query_params.get('debitor', None)

        print(parsing,betalergruppe,debitor)

        qs = Faktura.objects.all()
        if betalergruppe:
            qs = Faktura.objects.filter(rekvirent__betalergruppe__id=betalergruppe)#.order_by('-samlet_pris')
            # qs = qs.annotate(samlet_pris=Sum('analyser__samlet_pris'))
            # qs = qs.order_by('-samlet_pris')
        if parsing:
            qs = Faktura.objects.filter(parsing__id=parsing)#.order_by('-samlet_pris')
            # qs = qs.annotate(samlet_pris=Sum('analyser__samlet_pris'))
            # qs = qs.order_by('-samlet_pris')
        if debitor:
            qs = qs.filter(rekvirent__debitor__id=debitor)
        # else:
        qs = qs.annotate(samlet_pris=Sum('analyser__samlet_pris'))
        qs = qs.order_by('-samlet_pris')
        qs = qs.annotate(antal_analyser=Count('analyser'))
        return qs

    
    def perform_update(self, serializer):
    
        pdf_fil = self.request.data.get('pdf_fil')
        
        if pdf_fil:
            serializer.save(pdf_fil=pdf_fil)
        else:
            instance = serializer.save()       
    
class NestedFakturaViewSet(viewsets.ModelViewSet):
    # queryset = Faktura.objects.all()
    serializer_class = NestedFakturaSerializer

    def get_queryset(self):
        parsing = self.request.query_params.get('parsing', None)
        betalergruppe = self.request.query_params.get('betalergruppe', None)
        debitor = self.request.query_params.get('debitor', None)
        qs = Faktura.objects.all()

        print(parsing,betalergruppe,debitor)

        if parsing:
            qs = qs.filter(parsing__id=parsing)
        if betalergruppe:
            qs = qs.filter(rekvirent__betalergruppe__id=betalergruppe)
        if debitor:
            qs = qs.filter(rekvirent__debitor__id=debitor)
        
        qs = qs.annotate(samlet_pris=Sum('analyser__samlet_pris'))
        qs = qs.annotate(antal_analyser=Count('analyser', distinct=True))
        qs = qs.annotate(cpr=Count('analyser__CPR', distinct=True))
        qs = qs.order_by('-samlet_pris')

        # if parsing and betalergruppe:
        #     qs = Faktura.objects.filter(parsing__id=parsing, rekvirent__betalergruppe__id=betalergruppe)#.order_by('-samlet_pris')
        #     qs = qs.annotate(samlet_pris=Sum('analyser__samlet_pris'))
        #     qs = qs.annotate(cpr=Count('analyser__CPR', distinct=True))
        #     qs = qs.order_by('-samlet_pris')
        # elif parsing:
        #     qs = Faktura.objects.filter(parsing__id=parsing)
        #     qs = qs.annotate(samlet_pris=Sum('analyser__samlet_pris'))
        #     qs = qs.annotate(cpr=Count('analyser__CPR', distinct=True))
        #     qs = qs.order_by('-samlet_pris')
        # else:
        #     qs = Faktura.objects.all()
        # qs = qs.annotate(antal_analyser=Count('analyser', distinct=True))
        return qs

class SemiNestedFakturaViewSet(viewsets.ModelViewSet):
    queryset = Faktura.objects.all()
    serializer_class = SemiNestedFakturaSerializer

