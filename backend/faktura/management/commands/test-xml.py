
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

from backend.backend.faktura.extra.xml.XML_faktura import XMLFaktura
from backend.backend.faktura.models import Parsing


class Command(BaseCommand):
    help = 'Tests the xml faktura feature'

    def handle(self, *args, **options):

        call_command('generate-analyses-types-prices')
        call_command('generate-mock-data')

        parsing = Parsing.objects.first()


        XML_writer = XMLFaktura(parsing)

        XML_writer.create()