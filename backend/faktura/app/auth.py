import json
import logging
import time
from collections import namedtuple
from datetime import datetime, timedelta

import jwt
from dateutil.parser import parse
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group, User
from django.core import serializers
from django.db import models
from django.utils.timezone import now

from backend.faktura.models import Profile
from pprint import pprint

app_log = logging.getLogger('app')


def auth(username, password):
    """function that handles assigning correct user group to users logging in.
    Creates a user object that is used to sign for changes and handles of data
    Assigns a user group if not already"""
    if settings.DEBUG:
        return mock_auth(username, password)

    user = authenticate(username=username, password=password)

    if user is None:
        return None

    if not Profile.objects.filter(user=user).exists():
        Profile.objects.create(user=user)

    profile = Profile.objects.get(user=user)

    if hasattr(user, "username"):
        profile.username = user.username
    if hasattr(user, "display_name"):
        profile.display_name = user.display_name
    if hasattr(user, "email"):
        profile.email = user.email
    if hasattr(user, "title"):
        profile.title = user.title
    if hasattr(user, "telephone"):
        profile.telephone = user.telephone

    profile.er_akademiker = user.er_akademiker
    profile.er_admin = user.er_admin
    profile.er_bioanalytiker = user.er_bioanalytiker
    profile.er_bioinformatiker = user.er_bioinformatiker
    profile.er_sekretaer = user.er_sekretaer
    profile.er_studerende = user.er_studerende
    profile.save()

    return profile


def mock_auth(username, password):
    """handles mock users for local deployment"""
    # SIMULATE LOGIN DELAY
    time.sleep(1)

    if not Profile.objects.filter(username=username).exists():
        return None

    profile = Profile.objects.get(username=username)

    if profile and password == "1234":
        return profile

    return None
