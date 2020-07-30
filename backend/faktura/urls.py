from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from backend.faktura import views

# Create a router and register our viewsets with it.
router = DefaultRouter()

router.register(r'profiles', views.ProfileViewSet)

router.register(r'analyse-priser', views.AnalysePrisViewSet)

router.register(r'analyse-typer', views.AnalyseTypeViewSet)
router.register(r'analyse-typer-nested', views.NestedAnalyseTypeViewSet)

router.register(r'analyser', views.AnalyseViewSet)
router.register(r'analyser-nested', views.NestedAnalyseViewSet)

router.register(r'rekvirenter', views.RekvirentViewSet)
router.register(r'rekvirenter-nested', views.NestedRekvirentViewSet)

router.register(r'parsing', views.ParsingViewSet)
router.register(r'parsing-nested', views.NestedParsingViewSet)

router.register(r'faktura', views.FakturaViewSet)
router.register(r'faktura-nested', views.NestedFakturaViewSet)

router.register(r'faktura-status', views.FakturaStatusViewSet)

urlpatterns = [
    path('', include(router.urls)),
    url(r'^priser/', views.NewPricesView.as_view()),
    url(r'^priser-patoweb/', views.NewPatowebPricesView.as_view()),
    url(r'^download/$', views.download_file),
    url(r'^authenticate/', views.AuthenticateView.as_view()),
]
