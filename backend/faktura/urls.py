from posixpath import basename
from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from backend.faktura import views

# Create a router and register our viewsets with it.
router = DefaultRouter()

router.register(r'profiles', views.ProfileViewSet)

router.register(r'analyse-priser', views.AnalysePrisViewSet)

router.register(r'analyse-typer', views.AnalyseTypeViewSet, basename="Analysetyper")
router.register(r'analyse-typer-nested', views.NestedAnalyseTypeViewSet, basename='Analysetyper_Nested')

router.register(r'analyser', views.AnalyseViewSet)
router.register(r'analyser-nested', views.NestedAnalyseViewSet)

router.register(r'rekvirent', views.RekvirentViewSet)
router.register(r'rekvirent-nested', views.NestedRekvirentViewSet, basename="Rekvirenter_Nested")
router.register(r'rekvirent-missing', views.MissingRekvirentViewSet)

router.register(r'parsing', views.ParsingViewSet)
router.register(r'parsing-nested', views.NestedParsingViewSet)
# router.register(r'parsing-semi', views.SemiNestedParsingViewSet)

router.register(r'faktura', views.FakturaViewSet, basename="Faktura")
router.register(r'faktura-nested', views.NestedFakturaViewSet, basename="Faktura")
# router.register(r'faktura-semi', views.SemiNestedFakturaViewSet)

router.register(r'faktura-stat', views.FakturaStatViewSet, basename="Faktura statistics")

router.register(r'faktura-status', views.FakturaStatusViewSet)

# router.register(r'region', views.RegionViewSet)

router.register(r'betalergruppe', views.BetalergruppeViewSet, basename="Betalergruppe")
router.register(r'betalergruppe-nested', views.NestedBetalergruppeViewSet)

router.register(r'debitor', views.DebitorViewSet, basename="Debitor")

# router.register(r'bgrp-in-parse-price', views.BetalergrpInParseWithPriceViewSet)

# router.register(r'testpp', views.BigPPVS, basename='testpp')

urlpatterns = [
    path('', include(router.urls)),
    url(r'^priser/', views.NewPricesView.as_view()),
    url(r'^priser-patoweb/', views.NewPatowebPricesView.as_view()),
    url(r'^download/$', views.download_file),
    url(r'^authenticate/', views.AuthenticateView.as_view()),
    url(r'^send/', views.SendFaktura.as_view()),
    url(r'^rerun/', views.RerunMangelliste.as_view()),
]
