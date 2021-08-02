import logging
from backend.faktura.models.debitor import Debitor
from rest_framework import viewsets
from django.db.models import Count, Sum, Q

from backend.faktura.models import Faktura
from backend.faktura.serializers import FakturaSerializer, NestedFakturaSerializer, SemiNestedFakturaSerializer
logger = logging.getLogger(__name__)

class FakturaViewSet(viewsets.ModelViewSet):
    # queryset = Faktura.objects.all()
    serializer_class = FakturaSerializer

    def get_queryset(self):
        parsing = self.request.query_params.get('parsing', None)
        betalergruppe = self.request.query_params.get('betalergruppe', None)
        debitor = self.request.query_params.get('debitor', None)

        print('Fakturaviewset:', parsing, betalergruppe, debitor)

        qs = Faktura.objects.all()
        # if betalergruppe:
        #     qs = Faktura.objects.filter(rekvirent__betalergruppe__id=betalergruppe)#.order_by('-samlet_pris')
        #     # qs = qs.annotate(samlet_pris=Sum('analyser__samlet_pris'))
        #     # qs = qs.order_by('-samlet_pris')
        # if parsing:
        #     qs = Faktura.objects.filter(parsing__id=parsing)#.order_by('-samlet_pris')
        #     # qs = qs.annotate(samlet_pris=Sum('analyser__samlet_pris'))
        #     # qs = qs.order_by('-samlet_pris')
        if debitor:
            chosenDebitor = Debitor.objects.get(pk=debitor)
            # Tæl ikke analyser hvis type ikke faktureres til pågældende region med i prisudregningen
            if chosenDebitor.region == 'Hovedstaden':
                excludeQ = 'analyser__analyse_type__regionh'
            elif chosenDebitor.region == 'Sjælland':
                excludeQ = 'analyser__analyse_type__sjaelland'
            elif chosenDebitor.region == 'Syddanmark':
                excludeQ = 'analyser__analyse_type__syddanmark'
            elif chosenDebitor.region == 'Nordjylland':
                excludeQ = 'analyser__analyse_type__nordjylland'
            elif chosenDebitor.region == 'Midtjylland':
                excludeQ = 'analyser__analyse_type__midtjylland'
            qs = qs.filter(rekvirent__debitor__id=debitor)
            qs = qs.annotate(samlet_pris=Sum('analyser__samlet_pris'), filter=Q(excludeQ=False))
        else:
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
        # betalergruppe = self.request.query_params.get('betalergruppe', None)
        debitor = self.request.query_params.get('debitor', None)
        qs = Faktura.objects.all()

        # logger.info(parsing,debitor)

        if parsing:
            qs = qs.filter(parsing__id=parsing)
        # if betalergruppe:
        #     qs = qs.filter(rekvirent__betalergruppe__id=betalergruppe)
        if debitor:
            chosenDebitor = Debitor.objects.get(pk=debitor)
            logger.info(chosenDebitor)
            qs = qs.filter(rekvirent__debitor__id=debitor)
            # Tæl ikke analyser hvis type ikke faktureres til pågældende region med i prisudregningen
            excludeDict = {
                'Hovedstaden': Q(analyser__analyse_type__regionh=True),
                'Sjælland': Q(analyser__analyse_type__sjaelland=True),
                'Syddanmark': Q(analyser__analyse_type__syddanmark=True),
                'Nordjylland': Q(analyser__analyse_type__nordjylland=True),
                'Midtjylland': Q(analyser__analyse_type__midtjylland=True)
            }
            excludeQ = excludeDict.get(chosenDebitor.region, Q(True))
            qs = qs.annotate(samlet_pris=Sum('analyser__samlet_pris', filter=excludeQ))
        else:
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

