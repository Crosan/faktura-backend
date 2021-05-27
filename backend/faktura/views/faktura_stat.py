from rest_framework import viewsets
from django.db.models import Count, Sum

from backend.faktura.models import Faktura, Analyse, AnalyseType
from backend.faktura.serializers import AnalyseSerializer


class FakturaStatViewSet(viewsets.ModelViewSet):
    # queryset = Faktura.objects.all()
    serializer_class = AnalyseSerializer

    def get_queryset(self):
        faktura = self.request.query_params.get('faktura', None)
        if faktura:
            qs = Analyse.objects.filter(faktura_id=faktura)
            qs = qs.aggregate(types=Count('analyse_type'))
            # qs = qs.annotate(samlet_pris=Sum('analyser__samlet_pris'))
            # qs = qs.order_by('-samlet_pris')
            # qs = qs.annotate(antal_analyser=Count('analyser'))
        else:
            qs = Analyse.objects.all()
        return qs

    
    


