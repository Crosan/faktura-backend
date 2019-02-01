from rest_framework import viewsets

from backend.backend.models import Profile
from backend.backend.serializers.profile import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
