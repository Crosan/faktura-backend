from backend.faktura.extra.parser import Parser
from rest_framework import views, status
from rest_framework.response import Response
from django.core import serializers
import threading

from backend.faktura.models import *

import json
from rest_framework.response import Response
from rest_framework import status
import pytz
from pytz import timezone
from django.core.management import call_command
from datetime import datetime


class RerunMangelliste(views.APIView):    

    def get(self, request, *args, **kwargs):
        # print(request)
        # print(request.query_params.get('faktura', ""))
        parsing = request.query_params.get('parsing', "")
        print(parsing)
        # print(fakturas_to_send)
        # call_command('send-faktura') # Old, commented out by RS 2021-05-10
        # sender = FakturaSender()
        # sender.handle(selectedFakts=fakturas_to_send)
        # if parsing:
        #     call_command('rerun-mangelliste', settings={'parsing' : parsing})
        # else:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)
        # print('returning')


        parsing_obj = Parsing.objects.get(id=parsing)
        print('Appending to:', parsing_obj)
    
        t = threading.Thread(target=self.parseWrap, args=[parsing_obj])
        t.start()
        # return True
        # Parser.parse(parsing_obj)
        
        return Response(status=status.HTTP_200_OK)

    def parseWrap(self, parsing_object):
        print('wrapper called with path: %s' % parsing_object)
        parser = Parser()
        try:
            parser.parse(parsing_object, file_path=parsing_object.mangel_liste_fil, rerun=True)
        except:
            parsing_object.status = 'Fejlet: Ukendt fejl'
            parsing_object.save()

        
        
