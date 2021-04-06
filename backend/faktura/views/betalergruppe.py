from rest_framework import viewsets

from backend.faktura.models import Betalergruppe
from backend.faktura.serializers import BetalergruppeSerializer, NestedBetalergruppeSerializer

class BetalergruppeViewSet(viewsets.ModelViewSet):
    queryset = Betalergruppe.objects.all()
    serializer_class = BetalergruppeSerializer
    
class NestedBetalergruppeViewSet(viewsets.ModelViewSet):
    queryset = Betalergruppe.objects.all()
    serializer_class = NestedBetalergruppeSerializer