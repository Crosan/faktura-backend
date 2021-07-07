from rest_framework import viewsets
from django.db.models import Count, Sum, Q

from backend.faktura.models import Debitor
from backend.faktura.serializers import DebitorSerializer


class DebitorViewSet(viewsets.ModelViewSet):
    # queryset = Betalergruppe.objects.all()
    serializer_class = DebitorSerializer

    def get_queryset(self):
        EAN_nummer = self.request.query_params.get('ean', None)
        parsing = self.request.query_params.get('parsing', None)
        # print(parsing)
        if EAN_nummer:
            qs = Debitor.objects.filter(GLN_nummer=EAN_nummer)
        # else:
        #     qs = Debitor.objects.all()
        # return qs
    
        # print(parsing)
        elif parsing:
            qs = Debitor.objects.all(
                                           ).annotate(antal=Count('rekvirenter__fakturaer', filter=Q(rekvirenter__fakturaer__parsing__id=parsing), distinct=True)
                                           ).annotate(antal_unsent=Count('rekvirenter__fakturaer', filter=(Q(rekvirenter__fakturaer__parsing__id=parsing) & Q(rekvirenter__fakturaer__status=10)), distinct=True)
                                           ).annotate(sum_total=Sum('rekvirenter__fakturaer__analyser__samlet_pris', filter=Q(rekvirenter__fakturaer__parsing__id=parsing))
                                           ).annotate(sum_unsent=Sum('rekvirenter__fakturaer__analyser__samlet_pris', filter=(Q(rekvirenter__fakturaer__parsing__id=parsing) & Q(rekvirenter__fakturaer__status=10)))
                                           ).filter(antal__gt=0).order_by('-sum_total')
        else:
            qs = Debitor.objects.all(
                                          ).annotate(sum_total=Sum('rekvirenter__fakturaer__analyser__samlet_pris', filter=Q(rekvirenter__fakturaer__parsing__id=parsing))
                                          ).order_by('navn')
        return qs