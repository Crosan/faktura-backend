from rest_framework import viewsets

from backend.backend.models import AnalysePris
from backend.backend.serializers import AnalysePrisSerializer


class AnalysePrisViewSet(viewsets.ModelViewSet):
    queryset = AnalysePris.objects.all()
    serializer_class = AnalysePrisSerializer
