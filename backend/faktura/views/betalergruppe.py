from rest_framework import viewsets

from backend.faktura.models import Betalergruppe
from backend.faktura.serializers import BetalergruppeSerializer

class BetalergruppeViewSet(viewsets.ModelViewSet):
    queryset = Betalergruppe.objects.all()
    serializer_class = BetalergruppeSerializer
    
