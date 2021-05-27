
from django.core.management.base import BaseCommand, CommandError
from django.http import response
from backend.faktura.models import *
from datetime import timedelta
from django.core.management import call_command
from django.conf import settings
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
import pytz
import logging
import threading

logger = logging.getLogger("app")

from backend.faktura.extra.parser import Parser


class Command(BaseCommand):
    help = 'Processes the mangelliste for the specified parsing'

    # def add_arguments(self, parser):
    #     parser.add_argument('--file', dest="file_path", required=False,
    #                         help='Path to excel file to parse (used for testing purposes).')
    
        
    def handle(self, *args, **kwargs):
        if not 'parsing' in kwargs['settings'].keys():
            print('no')
            return #Response(status=status.HTTP_400_BAD_REQUEST)
        parsing = kwargs['settings']['parsing']
        parsing_object = Parsing.objects.get(id=parsing)

        t = threading.Thread(target=self.wrap, args=[kwargs["file_path"]])
        t.start()


        # return response(status=status.HTTP_400_BAD_REQUEST)
    
    def wrap(self, file_path):
        print('wrapper called with path: %s' % file_path)
        parser = Parser()
        parser.parse(file_path=file_path)

