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
        call_command('send-faktura')

        return Response(status=status.HTTP_200_OK)


        
        
        
        
