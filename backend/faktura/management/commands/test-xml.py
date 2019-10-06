
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

from backend.faktura.extra.xml.XML_faktura import XMLFaktura
from backend.faktura.models import Parsing


class Command(BaseCommand):
    help = 'Tests the xml faktura feature'

    def handle(self, *args, **options):

        parsing = Parsing.objects.first()

        XML_writer = XMLFaktura(parsing)

        XML_writer.create()