
from django.core.management.base import BaseCommand, CommandError
from backend.backend.models import *
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

        call_command('generate-data')
        
        analyseType1 = AnalyseType.objects.get(pk=1)
        
        rekvirent1 = Rekvirent.objects.get(pk=1)
        
        analyse1 = Analyse.objects.create(antal=2, rekvisitions_dato=now(), afregnings_dato=now(), analyse_type=analyseType1, rekvirent=rekvirent1)
