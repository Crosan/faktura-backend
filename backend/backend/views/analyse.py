from rest_framework import viewsets

from backend.backend.models import Analyse
from backend.backend.serializers import AnalyseSerializer, NestedAnalyseSerializer


class AnalyseViewSet(viewsets.ModelViewSet):
    queryset = Analyse.objects.all()
    serializer_class = AnalyseSerializer
    
class NestedAnalyseViewSet(viewsets.ModelViewSet):
    queryset = Analyse.objects.all()
    serializer_class = NestedAnalyseSerializer
