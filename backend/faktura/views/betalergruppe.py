from rest_framework import viewsets
from django.db.models import Count, Sum, Q

from backend.faktura.models import Betalergruppe
from backend.faktura.serializers import BetalergruppeSerializer, NestedBetalergruppeSerializer, PPBetalergruppeSerializer


class BetalergruppeViewSet(viewsets.ModelViewSet):
    # queryset = Betalergruppe.objects.all()
    serializer_class = BetalergruppeSerializer

    def get_queryset(self):
        parsing = self.request.query_params.get('parsing', None)
        # print(parsing)
        if parsing:
            qs = Betalergruppe.objects.all().annotate(sum_total=Sum('rekvirenter__fakturaer__analyser__samlet_pris', filter=Q(rekvirenter__fakturaer__parsing__id=parsing))
                                           ).annotate(sum_unsent=Sum('rekvirenter__fakturaer__analyser__samlet_pris', filter=Q(rekvirenter__fakturaer__parsing__id=parsing) & Q(rekvirenter__fakturaer__status=10))
                                           ).annotate(antal=Count('rekvirenter__fakturaer', filter=Q(rekvirenter__fakturaer__parsing__id=parsing))
                                           ).annotate(antal_unsent=Count('rekvirenter__fakturaer', filter=Q(rekvirenter__fakturaer__parsing__id=parsing) & Q(rekvirenter__fakturaer__status=10))
                                           ).order_by('-sum_total')
        else:
            qs = Betalergruppe.objects.all()
        return qs
    


class NestedBetalergruppeViewSet(viewsets.ModelViewSet):
    queryset = Betalergruppe.objects.all()
    serializer_class = NestedBetalergruppeSerializer


class BetalergrpInParseWithPriceViewSet(viewsets.ModelViewSet):
    # queryset = Betalergruppe.objects.all().annotate(sum_total=Sum('rekvirenter__fakturaer__samlet_pris'))
    # queryset = Betalergruppe.objects.all().annotate(sum_total=Sum(
    #     'rekvirenter__fakturaer__samlet_pris', filter=Q(rekvirenter__fakturaer__parsing__id=3)))
    queryset = Betalergruppe.objects.all().annotate(sum_total=Sum(
        'rekvirenter__fakturaer__analyser__samlet_pris', filter=Q(rekvirenter__fakturaer__parsing__id=3)))

    # def get_queryset(self):
    #     print(self.kwargs)
    #     return Betalergruppe.objects.all().annotate(sum_total=Sum('rekvirenter__fakturaer__samlet_pris'))

    # def retrieve(self, request, *args, **kwargs):

    # def get_queryset(self):
    #         """
    #         Optionally restricts the returned purchases to a given user,
    #         by filtering against a `username` query parameter in the URL.
    #         """
    # parsingID = self.request.query_params.get('parsingID')
    # if username is not None:
    #     queryset = Betalergruppe.objects.all().annotate(sum_total=Sum('rekvirenter__fakturaer__samlet_pris', filter=Q(rekvirenter__fakturaer__parsing__id=parsingID)))
    # else:
    #     queryset = Betalergruppe.objects.all().annotate(sum_total=Sum('rekvirenter__fakturaer__samlet_pris'))
    # return queryset

    serializer_class = PPBetalergruppeSerializer
    # serializer_class = BetalergruppeSerializer


class PPVS(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        queryset = Betalergruppe.objects.all().annotate(sum_total=Sum(
            'rekvirenter__fakturaer__samlet_pris', filter=Q(rekvirenter__fakturaer__parsing__id=pk)))
        # user = get_object_or_404(queryset, pk=pk)
        # serializer = UserSerializer(user)
        serializer = PPBetalergruppeSerializer
        return Response(serializer.data)
