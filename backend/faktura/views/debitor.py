from rest_framework import viewsets
from django.db.models import Count, Sum, Q

from backend.faktura.models import Debitor
from backend.faktura.serializers import DebitorSerializer


class DebitorViewSet(viewsets.ModelViewSet):
    # queryset = Betalergruppe.objects.all()
    serializer_class = DebitorSerializer

    def get_queryset(self):
        EAN_nummer = self.request.query_params.get('ean', None)
        # print(parsing)
        if EAN_nummer:
            qs = Debitor.objects.filter(GLN_nummer=EAN_nummer)
        else:
            qs = Debitor.objects.all()
        return qs
    