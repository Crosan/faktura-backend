from django.db.models.query import QuerySet
from rest_framework import viewsets
from django.db.models import Count, Sum, Q

from backend.faktura.models import Debitor, Rekvirent
from backend.faktura.serializers import DebitorSerializer


class DebitorViewSet(viewsets.ModelViewSet):
    # queryset = Betalergruppe.objects.all()
    serializer_class = DebitorSerializer

    def get_queryset(self):
        EAN_nummer = self.request.query_params.get('ean', None)
        parsing = self.request.query_params.get('parsing', None)
        searchterm = self.request.query_params.get('q', None)
        searchRekvirent = self.request.query_params.get('r', None)
        # print(parsing)
        if EAN_nummer:
            qs = Debitor.objects.filter(GLN_nummer=EAN_nummer)
        elif searchterm:
            qs = Debitor.objects.filter(Q(debitor_nr__icontains=searchterm) | 
                                        Q(navn__icontains=searchterm) | 
                                        Q(GLN_nummer__icontains=searchterm) | 
                                        Q(region__icontains=searchterm) | 
                                        Q(adresse__icontains=searchterm))
        elif searchRekvirent:
            '''Attempts first to match on GLN-numbers, and if none are found, matches on name and address'''
            queryRekvirent = Rekvirent.objects.get(pk=int(searchRekvirent))
            a = Debitor.objects.none()
            if queryRekvirent.GLN_nummer:
                qs1 = Debitor.objects.filter(Q(GLN_nummer__icontains=queryRekvirent.GLN_nummer))
                print(qs1)
                if len(qs1) > 0:
                    return qs1
                # a = a.union(qs1)
            if queryRekvirent.shortname:
                qs2 = Debitor.objects.filter(Q(navn__icontains=queryRekvirent.shortname))
                a = a.union(qs2)
            if queryRekvirent.address:
                qs3 = Debitor.objects.filter(Q(adresse__icontains=' '.join(queryRekvirent.address.split()[:2]))) # Take the two first words of the name, usually streetname and -number
                a = a.union(qs3)
            return a
            # qs = Debitor.objects.filter((Q('queryRekvirent__GLN_nummer')) & Q(GLN_nummer__icontains=queryRekvirent.GLN_nummer)) |
            #                             (Q('queryRekvirent__shortname')) & Q(navn__icontains=queryRekvirent.shortname))|
            #                             (Q('queryRekvirent__address')) & Q(adresse__icontains=' '.join(queryRekvirent.address.split()[:2])))) # Tager de første to ord, oftest vejnavn og - & )nr
        # else:
        #     qs = Debitor.objects.all()
        # return qs
    
        # print(parsing)
        elif parsing:
            regionfilter = ((Q(region='Hovedstaden') & Q(rekvirenter__fakturaer__analyser__analyse_type__regionh=True)) |
                            (Q(region='Sjælland')    & Q(rekvirenter__fakturaer__analyser__analyse_type__sjaelland=True)) |
                            (Q(region='Syddanmark')  & Q(rekvirenter__fakturaer__analyser__analyse_type__syddanmark=True)) |
                            (Q(region='Midtjylland') & Q(rekvirenter__fakturaer__analyser__analyse_type__midtjylland=True)) |
                            (Q(region='Nordjylland') & Q(rekvirenter__fakturaer__analyser__analyse_type__nordjylland=True))|
                             Q(region=None))
            qs = Debitor.objects.all(
                                           ).annotate(antal=Count('rekvirenter__fakturaer', filter=Q(rekvirenter__fakturaer__parsing__id=parsing), distinct=True)  #TODO: filtrér analyser med typer der ikke skal faktureres til debitors region fra
                                           ).annotate(antal_unsent=Count('rekvirenter__fakturaer', filter=(Q(rekvirenter__fakturaer__parsing__id=parsing) & Q(rekvirenter__fakturaer__status=10)), distinct=True)
                                           ).annotate(sum_total=Sum('rekvirenter__fakturaer__analyser__samlet_pris', filter=(Q(rekvirenter__fakturaer__parsing__id=parsing) & regionfilter))
                                           ).annotate(sum_unsent=Sum('rekvirenter__fakturaer__analyser__samlet_pris', filter=(Q(rekvirenter__fakturaer__parsing__id=parsing) & Q(rekvirenter__fakturaer__status=10) & regionfilter))
                                           ).filter(antal__gt=0).order_by('-sum_total')
        else:
            qs = Debitor.objects.all(
                                          ).annotate(sum_total=Sum('rekvirenter__fakturaer__analyser__samlet_pris', filter=Q(rekvirenter__fakturaer__parsing__id=parsing))
                                          ).order_by('navn')
        return qs