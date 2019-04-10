from rest_framework import viewsets

from backend.faktura.models import AnalyseType
from backend.faktura.serializers import AnalyseTypeSerializer, NestedAnalyseTypeSerializer


class AnalyseTypeViewSet(viewsets.ModelViewSet):
    queryset = AnalyseType.objects.all()
    serializer_class = AnalyseTypeSerializer
    
class NestedAnalyseTypeViewSet(viewsets.ModelViewSet):
    queryset = AnalyseType.objects.all()
    serializer_class = NestedAnalyseTypeSerializer
