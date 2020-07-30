import json
import logging
import os
import time
from datetime import datetime, timedelta
from pprint import pprint

import jwt
import pytz
from django.conf import settings
from django.utils.timezone import now
from request_logging.decorators import no_logging
from rest_framework import status, views
from rest_framework.response import Response

from backend.faktura.app.auth import auth

app_log = logging.getLogger('app')


class AuthenticateView(views.APIView):
    authentication_classes = []
    permission_classes = []

    @no_logging()
    def post(self, request, *args, **kwargs):
        utc = pytz.UTC

        username = request.data['username']
        password = request.data['password']

        profile = auth(username, password)

        if profile is None:
            app_log.info('bad login: ' + username)
            return Response(status=status.HTTP_200_OK)
        elif profile.start_dato and now() < profile.start_dato:
            print("Too soon")
            app_log.info('bad login: ' + username)
            return Response(status=status.HTTP_200_OK)
        elif profile.slut_dato and now() > profile.slut_dato:
            print("Too late")
            app_log.info('bad login: ' + username)
            return Response(status=status.HTTP_200_OK)
        else:
            app_log.info('success login: ' + username)
            token = self.create_token(profile)
            return Response(data={"token": token}, status=status.HTTP_200_OK)

    def create_token(self, profile):
        # craft jwt token here
        if 'DJANGO_SECRET' in os.environ:
            secret = os.environ.get('DJANGO_SECRET')
        else:
            secret = settings.SECRET_KEY

        token = {
            "exp": now() + timedelta(hours=8),
            "profile": {
                "id": profile.id,
                "display_name": profile.display_name,
                "email": profile.email,
                "telephone": profile.telephone,
                "title": profile.title,
                'er_akademiker': profile.er_akademiker,
                'er_admin': profile.er_admin,
                'er_bioanalytiker': profile.er_bioanalytiker,
                'er_bioinformatiker': profile.er_bioinformatiker,
                'er_sekretaer': profile.er_sekretaer,
                'er_studerende': profile.er_studerende,
            }
        }

        encoded = jwt.encode(token, secret)

        return encoded
