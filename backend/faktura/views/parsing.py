from rest_framework import viewsets

from backend.faktura.models import Parsing
from backend.faktura.serializers import ParsingSerializer, NestedParsingSerializer, SemiNestedParsingSerializer


class ParsingViewSet(viewsets.ModelViewSet):
    queryset = Parsing.objects.all()
    serializer_class = ParsingSerializer
    
class NestedParsingViewSet(viewsets.ModelViewSet):
    queryset = Parsing.objects.all()
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