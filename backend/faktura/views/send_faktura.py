from rest_framework import views, status
from rest_framework.response import Response
from django.core import serializers

from backend.faktura.models import *

import json
import pandas as pd
from rest_framework.response import Response
from rest_framework import status
import pytz
from pytz import timezone
from django.core.management import call_command
from datetime import datetime

class SendFaktura(views.APIView):    

    def get(self, request, *args, **kwargs):
        # print(request)
        # print(request.query_params.get('faktura', ""))
        fakturas_to_send = request.query_params.get('faktura', "").split(',')
        # print(fakturas_to_send)
        # call_command('send-faktura') # Old, commented out by RS 2021-05-10
        call_command('send-single-faktura', settings={'selectedFakts' : fakturas_to_send})

        return Response(status=status.HTTP_200_OK)


        
        
        
        
