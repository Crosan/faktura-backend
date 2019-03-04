from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from backend.backend import views

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

urlpatterns = [
    path('', include(router.urls)),
]
