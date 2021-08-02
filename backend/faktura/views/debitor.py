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
        searchterm = self.request.query_params.get('q', None)
        # print(parsing)
        if EAN_nummer:
            qs = Debitor.objects.filter(GLN_nummer=EAN_nummer)
        elif searchterm:
            print(searchterm)
            qs = Debitor.objects.filter(Q(debitor_nr__icontains=searchterm) | Q(navn__icontains=searchterm) | Q(GLN_nummer__icontains=searchterm) | Q(region__icontains=searchterm))
        # else:
        #     qs = Debitor.objects.all()
        # return qs
    
        # print(parsing)
        elif parsing:
            regionfilter = {
                'Hovedstaden': Q(rekvirenter__fakturaer__analyser__analysetype__regionh=True),
                'Sjælland': Q(rekvirenter__fakturaer__analyser__analysetype__sjaelland=True),
                'Syddanmark': Q(rekvirenter__fakturaer__analyser__analysetype__syddanmark=True),
                'Midtjylland': Q(rekvirenter__fakturaer__analyser__analysetype__midtjylland=True),
                'Nordjylland': Q(rekvirenter__fakturaer__analyser__analysetype__nordjylland=True),
            }
            qs = Debitor.objects.all(
                                           ).annotate(antal=Count('rekvirenter__fakturaer', filter=Q(rekvirenter__fakturaer__parsing__id=parsing), distinct=True)  #TODO: filtrér analyser med typer der ikke skal faktureres til debitors region fra
                                           ).annotate(antal_unsent=Count('rekvirenter__fakturaer', filter=(Q(rekvirenter__fakturaer__parsing__id=parsing) & Q(rekvirenter__fakturaer__status=10)), distinct=True)
                                           ).annotate(sum_total=Sum('rekvirenter__fakturaer__analyser__samlet_pris', filter=(Q(rekvirenter__fakturaer__parsing__id=parsing) & (
                                                (Q(region='Hovedstaden') & Q(rekvirenter__fakturaer__analyser__analyse_type__regionh=True)) |
                                                (Q(region='Sjælland')    & Q(rekvirenter__fakturaer__analyser__analyse_type__sjaelland=True)) |
                                                (Q(region='Syddanmark')  & Q(rekvirenter__fakturaer__analyser__analyse_type__syddanmark=True)) |
                                                (Q(region='Midtjylland') & Q(rekvirenter__fakturaer__analyser__analyse_type__midtjylland=True)) |
                                                (Q(region='Nordjylland') & Q(rekvirenter__fakturaer__analyser__analyse_type__nordjylland=True)) 
                                           )))
                                           ).annotate(sum_unsent=Sum('rekvirenter__fakturaer__analyser__samlet_pris', filter=(Q(rekvirenter__fakturaer__parsing__id=parsing) & Q(rekvirenter__fakturaer__status=10)))
                                           ).filter(antal__gt=0).order_by('-sum_total')
        else:
            qs = Debitor.objects.all(
                                          ).annotate(sum_total=Sum('rekvirenter__fakturaer__analyser__samlet_pris', filter=Q(rekvirenter__fakturaer__parsing__id=parsing))
                                          ).order_by('navn')
        return qs