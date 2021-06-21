from rest_framework import viewsets
from django.db.models import Count, Sum, Q

from backend.faktura.models import AnalyseType
from backend.faktura.serializers import AnalyseTypeSerializer, NestedAnalyseTypeSerializer


class AnalyseTypeViewSet(viewsets.ModelViewSet):
    # queryset = AnalyseType.objects.all()
    serializer_class = AnalyseTypeSerializer

    def get_queryset(self):
        faktura = self.request.query_params.get('faktura', None)
        searchterm = self.request.query_params.get('q', None)
        # print(faktura)
        if faktura:
            qs = AnalyseType.objects.all().annotate(antal=Count('analyser', filter=Q(analyser__faktura__id = faktura))
                                         ).annotate(pris=Sum('analyser__samlet_pris', filter=Q(analyser__faktura__id = faktura))
                                         ).filter(antal__gt=0).order_by('-antal')
            # qs = Betalergruppe.objects.all(
            #                                ).annotate(antal=Count('rekvirenter__fakturaer', filter=Q(rekvirenter__fakturaer__parsing__id=parsing), distinct=True)
            #                                ).annotate(antal_unsent=Count('rekvirenter__fakturaer', filter=(Q(rekvirenter__fakturaer__parsing__id=parsing) & Q(rekvirenter__fakturaer__status=10)), distinct=True)
            #                                ).annotate(sum_total=Sum('rekvirenter__fakturaer__analyser__samlet_pris', filter=Q(rekvirenter__fakturaer__parsing__id=parsing))
            #                                ).annotate(sum_unsent=Sum('rekvirenter__fakturaer__analyser__samlet_pris', filter=(Q(rekvirenter__fakturaer__parsing__id=parsing) & Q(rekvirenter__fakturaer__status=10)))
            #                                ).order_by('-sum_total')
        elif searchterm:
            print(searchterm)
            qs = AnalyseType.objects.filter(Q(ydelses_kode__icontains=searchterm) | Q(ydelses_navn__icontains=searchterm) | Q(gruppering__icontains=searchterm) | Q(afdeling__icontains=searchterm))
        else:
            qs = AnalyseType.objects.all()
        return qs


class NestedAnalyseTypeViewSet(viewsets.ModelViewSet):
    # queryset = AnalyseType.objects.all()
    serializer_class = NestedAnalyseTypeSerializer

    def get_queryset(self):
        searchterm = self.request.query_params.get('q', None)
        if searchterm:
            print(searchterm)
            qs = AnalyseType.objects.filter(Q(ydelses_kode__icontains=searchterm) | Q(ydelses_navn__icontains=searchterm) | Q(gruppering__icontains=searchterm) | Q(afdeling__icontains=searchterm))
        else:
            qs = AnalyseType.objects.all()
        return qs
