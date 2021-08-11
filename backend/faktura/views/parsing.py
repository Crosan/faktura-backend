from rest_framework import viewsets
from django.db.models import Count, Sum, Q

from backend.faktura.models import Parsing
from backend.faktura.serializers import ParsingSerializer, NestedParsingSerializer, SemiNestedParsingSerializer


class ParsingViewSet(viewsets.ModelViewSet):
    queryset = Parsing.objects.all().annotate(antal_fakturaer=Count('fakturaer', distinct=True)
                                   ).annotate(antal_unknown=Count('fakturaer', filter=(Q(fakturaer__rekvirent__debitor=None)), distinct=True)
                                   ).annotate(samlet_pris=Sum('fakturaer__analyser__samlet_pris')
                                   ).order_by('-oprettet')
    serializer_class = ParsingSerializer
    
class NestedParsingViewSet(viewsets.ModelViewSet):
    queryset = Parsing.objects.all().order_by('-oprettet')
    serializer_class = NestedParsingSerializer

class SemiNestedParsingViewSet(viewsets.ModelViewSet):
    '''
    Returns parsing, nested only one level (i.e. fakturaer in parse is included, but analyser in fakturaer are not)
    '''
    queryset = Parsing.objects.all()
    serializer_class = SemiNestedParsingSerializer

# class BetalergrpInParseWithPriceParseViewSet(viewsets.ModelViewSet):
#     queryset = Betalergruppe.objects.all().annotate(sum_total=Sum('rekvirenter__fakturaer__samlet_pris')))
#     serializer_class = BetalergruppeSerializer