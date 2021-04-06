from rest_framework import viewsets

from backend.faktura.models import Faktura
from backend.faktura.serializers import FakturaSerializer, NestedFakturaSerializer, SemiNestedFakturaSerializer


class FakturaViewSet(viewsets.ModelViewSet):
    queryset = Faktura.objects.all()
    serializer_class = FakturaSerializer
    
    def perform_update(self, serializer):
    
        pdf_fil = self.request.data.get('pdf_fil')
        
        if pdf_fil:
            serializer.save(pdf_fil=pdf_fil)
        else:
            instance = serializer.save()       
    
class NestedFakturaViewSet(viewsets.ModelViewSet):
    queryset = Faktura.objects.all()
    serializer_class = NestedFakturaSerializer

class SemiNestedFakturaViewSet(viewsets.ModelViewSet):
    queryset = Faktura.objects.all()
    serializer_class = SemiNestedFakturaSerializer

