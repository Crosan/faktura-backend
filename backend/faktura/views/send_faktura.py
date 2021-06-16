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

import smbclient
from backend.faktura.extra.xml.XML_faktura_writer import XMLFakturaWriter

class SendFaktura(views.APIView):    

    def get(self, request, *args, **kwargs):
        # print(request)
        # print(request.query_params.get('faktura', ""))
        fakturas_to_send = request.query_params.get('faktura', "").split(',')
        # print(fakturas_to_send)
        # call_command('send-faktura') # Old, commented out by RS 2021-05-10
        # sender = FakturaSender()
        # sender.handle(selectedFakts=fakturas_to_send)
        call_command('send-single-faktura', settings={'selectedFakts' : fakturas_to_send})
        print('returning')

        return Response(status=status.HTTP_200_OK)


class FakturaSender():
    ''' Generates XML-representation of specified fakturas and uploads them to the SMB server 
    Is not used as of 25/05/21 (check this)'''

    serverLocation = r"//regionh.top.local/DFS/Systemer/SAP/SAP001/DIAC2SAP/Prod/"

    def writeXMLtoFile(self, xml, filename):
        ''' For testing/debugging purposes '''
        with open('C:\\Users\\RSIM0016\\Documents\\faktura\\xmltests\\%s.xml' % filename, 'w', encoding='utf-8') as f:
            f.write(xml)
    
    def uploadToSMBShare(self, content):
        ''' Uses the server location from the class namespace and generates a timestamped filename

        Parameters:
            content : XML-formatted text 
            
        Returns:
            True : If file was transferred without errors
            None : Otherwise'''
        filename = r'DIAFaktura_' + datetime.now().strftime("%Y%m%d_%H%M%S%f")[:-4] + '.xml'
        dst = self.serverLocation + filename
        # try:
        with smbclient.open_file(dst, mode="w", username="RGH-S-AutoDIAfaktura", password="JDQTS#wqzfg72396") as fd:
            fd.write(u"%s" % content)
        #     return True
        # except E:
        #     print(E)
        return None

    # def handle(self, *args, **options):
    def handle(self, selectedFakts):
        # self.print_env()
        
        # if not 'selectedFakts' in options['settings'].keys():
        #     print('no')
        #     return #Response(status=status.HTTP_400_BAD_REQUEST)

        # faktQS = Faktura.objects.filter(pk__in=options['settings']['selectedFakts'])
        faktQS = Faktura.objects.filter(pk__in=selectedFakts)
        # print(faktQS)

        # for faktura in faktQS:
        for i, fakt in enumerate(faktQS):
            XML_faktura_writer = XMLFakturaWriter() # Horrible hack, change this
            print(fakt)
            if not fakt.status == 10:
                continue
            x = XML_faktura_writer.create(fakt)
            self.writeXMLtoFile(x, str(fakt.id))
            # success = self.uploadToSMBShare(x)
            success = True
            if success:
                fakt.status = 20
                fakt.save()
            else:
                print('Failed up upload faktura "%s"' % str(fakt))

        # XML_faktura_writer.create(faktQS)

        return
        
        
        
