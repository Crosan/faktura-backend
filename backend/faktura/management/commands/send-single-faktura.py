import logging
import math
import re
from datetime import datetime

import smbclient
import sys

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

    # if settings.TESTING:
    serverLocation = r"\\regionh.top.local\DFS\Systemer\SAP\SAP001\DIAC2SAP\Prod\skalslettes\ "
    # else:
    #     serverLocation = r"\\regionh.top.local\DFS\Systemer\SAP\SAP001\DIAC2SAP\Prod\ "


    def writeXMLtoFile(self, xml, filename):
        ''' For testing/debugging purposes '''
        filename += '.xml'
        outpath = os.path.join(os.getcwd(), 'backend', 'media', 'xml_output', filename)
        logger.info('Writing xml file to: %s' % outpath)

        # with open('C:\\Users\\RSIM0016\\Documents\\faktura\\xmltests\\%s.xml' % filename, 'w', encoding='utf-8') as f:
        with open(outpath, 'w', encoding='utf-8') as f:
            f.write(xml)
    
    def uploadToSMBShare(self, content):
        ''' Uses the server location from the class namespace and generates a timestamped filename

        Parameters:
            content : XML-formatted text 
            
        Returns:
            True : If file was transferred without errors
            None : Otherwise'''

        logger.info('Sending faktura to: \n %s' % self.serverLocation)

        filename = r'DIAFaktura_' + datetime.now().strftime("%Y%m%d_%H%M%S%f")[:-4] + '.xml'
        dst = self.serverLocation[:-1] + filename

        try:
            with smbclient.open_file(dst, mode="w", encoding='utf-8') as fd:
                # fd.write(u"%s" % content)
                fd.write(content)
            return True
        except:
            # print('failed')
            # print("Unexpected error:", sys.exc_info()[0])
            logger.error("Unexpected error:", sys.exc_info()[0])
            return None

    def handle(self, *args, **options):
        # self.print_env()
        
        # if not 'selectedFakts' in options['settings'].keys():
        #     print('no')
        #     logger.error('Sendfaktura called with no faktura IDs')
        #     return #Response(status=status.HTTP_400_BAD_REQUEST)
        logger.info(str(options))

        # if not 'debitor' in options['settings'].keys():
        if not options['settings'].get('debitor', None):
            logger.error('Sendfaktura called with no debitor ID')
            return 

        # if not 'parsing' in options['settings'].keys():
        if not options['settings'].get('parsing', None):
            logger.error('Sendfaktura called with no parsing ID')
            return

        # faktQS = Faktura.objects.filter(
        #         rekvirent__debitor__id=int(options['settings']['debitor'])
        #     ).filter(
        #         parsing__id=int(options['settings']['parsing'])
        #     )

        chosenDebitor = Debitor.objects.get(pk=int(options['settings']['debitor']))

        analQS = Analyse.objects.filter(
                faktura__rekvirent__debitor__id=int(options['settings']['debitor'])
            ).filter(
                faktura__parsing__id=int(options['settings']['parsing'])
            )
        
        logger.info(analQS)
        logger.info(chosenDebitor)
        return

        faktQS = Faktura.objects.filter(pk__in=options['settings']['selectedFakts'])
        # print(faktQS)

        # TODO: Lav en global config

        # logger.info('Setting up SMB ClientConfig')
        # smbclient.ClientConfig(username=settings.SMB_USER, password=settings.SMB_PASS, skip_dfs=True)

        # Forbindelsen virker kun hvis man kører listdir en gang først. Jeg ved ikke hvorfor...
        # logger.info('Running listdir')
        # print(smbclient.listdir(path=r"\\regionh.top.local\DFS\Systemer\SAP\SAP001\DIAC2SAP\Prod"))

        logger.info('Starting loop')
        # for faktura in faktQS:
        for i, fakt in enumerate(faktQS):
            XML_faktura_writer = XMLFakturaWriter() 
            logger.info("Sending file: %s" % fakt)
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
                logger.error('Failed up upload faktura "%s"' % str(fakt))

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