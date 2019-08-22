
from django.core.management.base import BaseCommand, CommandError
from backend.faktura.models import *
from datetime import datetime, timedelta
from django.core.management import call_command
from django.conf import settings
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now
import pytz


class Command(BaseCommand):
    help = 'Populates the database with dummy data'

    def add_arguments(self, parser):
        parser.add_argument('-f', '--force', dest="force", action="store_true",
                            help='Override debug settings and always create dummy data.')

    def handle(self, *args, **options):
        print("Opretter mock data... ", end='', flush=True)
        
        analyseType1 = AnalyseType.objects.first()
        
        rekvirent1 = Rekvirent.objects.first()
        
        analyse1 = Analyse.objects.create(antal=2, CPR="p1", afregnings_dato=now(), svar_dato=now(), analyse_type=analyseType1)

        print("done")