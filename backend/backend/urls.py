from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from backend.backend import views

# Create a router and register our viewsets with it.
router = DefaultRouter()

router.register(r'profiles', views.ProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
