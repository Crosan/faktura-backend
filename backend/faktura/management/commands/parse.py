
from django.core.management.base import BaseCommand, CommandError
from backend.faktura.models import *
from datetime import timedelta
from django.core.management import call_command
from django.conf import settings
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist
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
    help = 'Populates the database with dummy data'

    def add_arguments(self, parser):
        parser.add_argument('--file', dest="file_path", required=False,
                            help='Path to excel file to parse (used for testing purposes).')
    
        
    def handle(self, *args, **kwargs):
        print("parse.py called with kwargs:", kwargs)
        # parser = Parser()
        print('now threaded')
        # parser = Parser()
        # print(kwargs['file_path'])
        t = threading.Thread(target=self.wrap, args=[kwargs["file_path"]])
        t.start()
        # parser.parse(None, kwargs["file_path"])
    
    def wrap(self, file_path):
        print('wrapper called with path: %s' % file_path)
        parser = Parser()
        parser.parse(file_path=file_path)
        
    
        
