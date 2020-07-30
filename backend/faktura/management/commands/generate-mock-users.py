import csv
import json
import os
import sys
from django.utils.timezone import now
from collections import namedtuple

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from backend.faktura.models import *

sys.path.insert(0, os.path.abspath(".."))


class Command(BaseCommand):
    help = 'Populates the database with mock users'

    ProfileType = namedtuple('Profile', ['id', 'user', 'start_dato', 'slut_dato', 'username', 'display_name', 'telephone', 'email', 'title', 'er_akademiker',
                                         'er_admin', 'er_bioanalytiker', 'er_bioinformatiker', 'er_sekretaer', 'er_studerende'])

    mock_profiles = [
        ProfileType(1, 1, now(), None, 'akademiker', "{} bruger".format("akademiker"),
                    "example@mail", "12341234", "developer", True, False, False, False, False, False),
        ProfileType(2, 2, now(), None, 'admin', "{} bruger".format("admin"), "12341234",
                    "example@mail", "developer", False, True, False, False, False, False),
        ProfileType(3, 3, now(), None, 'bioanalytiker', "{} bruger".format("bioanalytiker"),
                    "12341234", "example@mail", "developer", False, False, True, False, False, False),
        ProfileType(4, 4, now(), None, 'bioinformatiker', "{} bruger".format("bioinformatiker"),
                    "12341234", "example@mail", "developer", False, False, False, True, False, False),
        ProfileType(5, 5, now(), None, 'sekretær', "{} bruger".format(
            "sekretær"), "12341234", "example@mail", "developer", False, False, False, False, True, False),
        ProfileType(6, 6, now(), None, 'studerende', "{} bruger".format("studerende"),
                    "12341234", "example@mail", "developer", False, False, False, False, False, True)
    ]

    def handle(self, *args, **options):

        print("Opretter mock brugere... ", end='', flush=True)

        for p in self.mock_profiles:
            user = User.objects.create(username=p.username)

            Profile.objects.get_or_create(
                user=user,
                username=p.username,
                display_name=p.display_name,
                title=p.title,
                telephone=p.telephone,
                email=p.email,
                er_akademiker=p.er_akademiker,
                er_admin=p.er_admin,
                er_bioanalytiker=p.er_bioanalytiker,
                er_bioinformatiker=p.er_bioinformatiker,
                er_sekretaer=p.er_sekretaer,
                er_studerende=p.er_studerende
            )

        print("done")
