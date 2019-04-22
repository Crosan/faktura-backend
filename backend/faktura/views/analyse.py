from rest_framework import viewsets

from backend.faktura.models import Analyse
from backend.faktura.serializers import AnalyseSerializer, NestedAnalyseSerializer


class AnalyseViewSet(viewsets.ModelViewSet):
    queryset = Analyse.objects.all()
    serializer_class = AnalyseSerializer
    
class NestedAnalyseViewSet(viewsets.ModelViewSet):
    queryset = Analyse.objects.all()
    serializer_class = NestedAnalyseSerializer
