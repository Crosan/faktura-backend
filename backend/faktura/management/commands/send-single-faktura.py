import logging
import math
import re
from datetime import datetime

import smbclient

import pandas as pd
import pytz
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import now
from pytz import timezone
from django.core.files.base import ContentFile

from backend.faktura.extra.xml.XML_faktura_writer import XMLFakturaWriter
from backend.faktura.models import *
# from backend.faktura.models import Parsing


logger = logging.getLogger(__name__)
local_tz = pytz.timezone('Europe/Copenhagen')


class Command(BaseCommand):
    ''' Generates XML-representation of specified fakturas and uploads them to the SMB server '''

    serverLocation = r"//regionh.top.local/DFS/Systemer/SAP/SAP001/DIAC2SAP/Prod/"

    def writeXMLtoFile(self, xml, filename):
        ''' For testing/debugging purposes '''
        with open('C:\\Users\\RSIM0016\\Documents\\faktura\\xmltests\\%s.xml' % filename, 'w') as f:
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

    def handle(self, *args, **options):
        # self.print_env()
        
        if not 'selectedFakts' in options['settings'].keys():
            print('no')
            return #Response(status=status.HTTP_400_BAD_REQUEST)

        faktQS = Faktura.objects.filter(pk__in=options['settings']['selectedFakts'])
        # print(faktQS)

        # for faktura in faktQS:
        for i, fakt in enumerate(faktQS):
            XML_faktura_writer = XMLFakturaWriter() # Horrible hack, change this
            print(fakt)
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

        # try:
        #     conn = self.setup_smb_conn()
        # except:
        #     parsings = self.get_unprocessed_parsings()

        #     xml_fakturas = self.process_parsings(parsings)

        #     django_xml_fakturas = self.generate_django_xml_fakturas(xml_fakturas)

        #     print("prepared fakturas")

        #     return
        #     None

        # conn.connect(os.environ.get('FTP_HOST'), 445)

        # print("login successful")

        # parsings = self.get_unprocessed_parsings()

        # xml_fakturas = self.process_parsings(parsings)

        # django_xml_fakturas = self.generate_django_xml_fakturas(xml_fakturas)

        # print("prepared fakturas")

        # ## Overvej her at slette successfuldt sendte fakturaer da de kan fylde ganske meget

        # upload_dir = os.environ.get('FTP_UPLOAD_DIR')
        # worker = Worker(conn, upload_dir, django_xml_fakturas)

        # worker.run()