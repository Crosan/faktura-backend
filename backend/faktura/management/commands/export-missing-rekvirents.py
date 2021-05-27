
from django.core.management.base import BaseCommand, CommandError
from backend.faktura.models import *
from datetime import timedelta
from django.core.management import call_command
from django.conf import settings
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
import pytz
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import datetime
import math
import logging
import threading

logger = logging.getLogger("app")

from backend.faktura.extra.parser import Parser


class Command(BaseCommand):
    help = 'Generates an excel-file in /media containing the rekvirents with unknown debitor number'

    # def add_arguments(self, parser):
    #     parser.add_argument('--file', dest="file_path", required=False,
    #                         help='Path to excel file to parse (used for testing purposes).')
    
        
    def handle(self, *args, **kwargs):
        print("Exporting rekvirents with missing debitor or betalergruppe\nCalled with kwargs:", kwargs)
        filt = Q(debitor_nr = None) | Q(betalergruppe = None)
        queryset = Rekvirent.objects.filter(filt)
        df = pd.DataFrame(list(queryset.values('shortname', 'GLN_nummer', 'rekv_nr', 'betalergruppe__navn', 'debitor_nr')))
        df = df.rename(columns={'shortname' : 'Rekvirentnavn',
                                'GLN_nummer' : 'GLN-nummer', 
                                'rekv_nr' : 'Rekvirentnummer', 
                                'betalergruppe__navn' : 'Betalergruppe',
                                'debitor_nr' : 'Debitornummer'})
        file_path = os.path.join(os.getcwd(), 'backend', 'media', 'missing_rekvirents.xlsx')
        df.to_excel(file_path, index=False)
        print('Done')

    
        
