# my_app/authentication.py
import os

import jwt
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import authentication, exceptions

from backend.faktura.models import Profile


class FakturaAuthentication(authentication.BaseAuthentication):
    """function that handles a user already being logged in"""

    def authenticate(self, request):
        # get the username request header
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:  # no username passed in request headers
            return None  # authentication did not succeed

        token = token.encode()

        if 'DJANGO_SECRET' in os.environ:
            secret = os.environ.get('DJANGO_SECRET')
        else:
            secret = settings.SECRET_KEY

        try:
            decoded_token = jwt.decode(token, secret)
            profile = Profile.objects.get(
                pk=decoded_token['profile']['id'])  # get the user
        except Profile.DoesNotExist:
            # raise exception if user does not exist
            raise exceptions.AuthenticationFailed('No such profile')

        return (profile.user, None)  # authentication successful
