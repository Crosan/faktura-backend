from rest_framework import viewsets

from backend.faktura.models import Profile
from backend.faktura.serializers import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
