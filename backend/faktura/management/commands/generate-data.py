
from django.core.management.base import BaseCommand, CommandError
from backend.faktura.models import *
from django.core.management import call_command
from django.conf import settings
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now
import pandas as pd
import math
import pytz
from pytz import timezone
from datetime import datetime


class Command(BaseCommand):
    help = 'Populates the database with data'

    def handle(self, *args, **options):
        call_command('generate-analyses-types-prices')

        if settings.DEVELOPMENT or settings.TESTING:
            call_command('generate-mock-data')