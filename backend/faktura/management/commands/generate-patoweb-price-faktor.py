
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
        print("Opretter patoweb price faktors... ", end='', flush=True)
        
        faktors = PatowebPrisFaktor(RgH=9.69, praksis=9.69, grønland=9.69, andet=1.10)
        faktors.save()

        print("done")