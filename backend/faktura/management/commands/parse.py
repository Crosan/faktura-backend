
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
        parser.add_argument('--file', dest="file_path", required=False,
                            help='Path to excel file to parse (used for testing purposes).')

    def handle(self, *args, **options):

        print("HEY")
