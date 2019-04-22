from rest_framework import viewsets

from backend.faktura.models import AnalysePris
from backend.faktura.serializers import AnalysePrisSerializer


class AnalysePrisViewSet(viewsets.ModelViewSet):
    queryset = AnalysePris.objects.all()
    serializer_class = AnalysePrisSerializer
