from rest_framework import viewsets

from backend.faktura.models import Parsing
from backend.faktura.serializers import ParsingSerializer, NestedParsingSerializer


class ParsingViewSet(viewsets.ModelViewSet):
    queryset = Parsing.objects.all()
    serializer_class = ParsingSerializer
    
class NestedParsingViewSet(viewsets.ModelViewSet):
    queryset = Parsing.objects.all()
    serializer_class = NestedParsingSerializer
