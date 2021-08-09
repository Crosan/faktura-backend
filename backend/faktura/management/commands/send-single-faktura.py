import logging
import math
import re
from datetime import datetime
import time

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
from django.db.models import Q

from backend.faktura.extra.xml.XML_faktura_writer import XMLFakturaWriter
from backend.faktura.models import *
# from backend.faktura.models import Parsing


logger = logging.getLogger(__name__)
local_tz = pytz.timezone('Europe/Copenhagen')


class Command(BaseCommand):
    ''' Generates XML-representation of specified fakturas and uploads them to the SMB server '''

    # if settings.TESTING:
    # serverLocation = r"\\regionh.top.local\DFS\Systemer\SAP\SAP001\DIAC2SAP\Prod\skalslettes\ "
    serverLocation = os.path.join(settings.PATH, settings.LOCALPATH)
    logger.info('Serverlocation is: ' + serverLocation)
    # else:
    #     serverLocation = r"\\regionh.top.local\DFS\Systemer\SAP\SAP001\DIAC2SAP\Prod\ "
    # logger.info('Resetting connection cache')
    # smbclient.reset_connection_cache()


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


        

        filename = r'DIAFaktura_' + datetime.now().strftime("%Y%m%d_%H%M%S%f")[:-4] + '.xml'
        dst = self.serverLocation[:-1] + filename #Remove trailing space in server path

        logger.info('Sending faktura to: \n %s' % dst)

        try:
            with open(dst, 'w', encoding='utf-8') as f:
                f.write(content)
            # with smbclient.open_file(dst, mode="w", encoding='utf-8') as fd:
            #     # fd.write(u"%s" % content)
            #     fd.write(content)
            # smbclient.delete_session(r'\\regionh.top.local')
            return True
        except:
            # print('failed')
            # print("Unexpected error:", sys.exc_info()[0])
            logger.error("Unexpected error:" + str(sys.exc_info()[0]))
            return None

    def handle(self, *args, **options):
        # self.print_env()
        
        # if not 'selectedFakts' in options['settings'].keys():
        #     print('no')
        #     logger.error('Sendfaktura called with no faktura IDs')
        #     return #Response(status=status.HTTP_400_BAD_REQUEST)
        logger.info(str(options))

        debitor = options['settings'].get('debitor', None)
        parse = options['settings'].get('parsing', None)

        # if not 'debitor' in options['settings'].keys():
        if not debitor:
            logger.error('Sendfaktura called with no debitor ID')
            return 

        # if not 'parsing' in options['settings'].keys():
        if not parse:
            logger.error('Sendfaktura called with no parsing ID')
            return

        faktQS = Faktura.objects.filter(
                rekvirent__debitor__id=int(debitor)
            ).filter(
                parsing__id=int(parse)
            ).filter(
                status=10
            )

        chosenDebitor = Debitor.objects.get(pk=int(debitor))
        # excludeDict = {
        #         'Hovedstaden': Q(analyse_type__regionh=True),
        #         'Sjælland': Q(analyse_type__sjaelland=True),
        #         'Syddanmark': Q(analyse_type__syddanmark=True),
        #         'Nordjylland': Q(analyse_type__nordjylland=True),
        #         'Midtjylland': Q(analyse_type__midtjylland=True)
        #     }
        # excludeQ = excludeDict.get(chosenDebitor.region, Q(True))

        analQS = Analyse.objects.filter(
                faktura__rekvirent__debitor__id=int(debitor)
            ).filter(
                faktura__parsing__id=int(parse)
            ).filter(
                faktura__status=10
            # ).filter(
            #     excludeQ
            )
        
        logger.info(analQS)
        logger.info(chosenDebitor)

        # faktQS = Faktura.objects.filter(pk__in=options['settings']['selectedFakts'])
        # print(faktQS)

        # TODO: Lav en global config

        # logger.info('Setting up SMB ClientConfig')
        # smbclient.ClientConfig(username=settings.SMB_USER, password=settings.SMB_PASS, skip_dfs=True)

        SMB_USER = os.environ.get('SMB_USER')
        SMB_PASS = os.environ.get('SMB_PASS')
        logger.info(SMB_USER)
        logger.info(SMB_PASS)

        # Forbindelsen virker kun hvis man kører listdir en gang først. Jeg ved ikke hvorfor...
        # dirlisting = smbclient.listdir(path=r"\\regionh.top.local\DFS\Systemer\SAP\SAP001\DIAC2SAP\Prod")
        logger.info('Registering session')
        thisSession = smbclient.register_session(r'box1-fls.regionh.top.local', username=SMB_USER, password=SMB_PASS)
        logger.info(thisSession)
        time.sleep(1)
        logger.info('Running listdir')
        dirlisting = smbclient.listdir(path=r"\\regionh.top.local\DFS\Systemer\SAP\SAP001\DIAC2SAP\Prod\skalslettes")
        logger.info(dirlisting)

        logger.info('Starting writing the faktura')
        XML_faktura_writer = XMLFakturaWriter()


        try:
            output = XML_faktura_writer.create(chosenDebitor, analQS)
            self.writeXMLtoFile(output, parse + '_' +  chosenDebitor.debitor_nr)
            self.uploadToSMBShare(output)
            for faktura in faktQS:
                faktura.status = 20
                faktura.save()
            success = True
            logger.info('Running listdir')
            dirlisting = smbclient.listdir(path=r"\\regionh.top.local\DFS\Systemer\SAP\SAP001\DIAC2SAP\Prod\skalslettes")
            logger.info(dirlisting)
        except:
            logger.error('Writing or uploading xml file failed')
            success = False
        finally:
            logger.info('Deleting session...')
            smbclient.delete_session(r'box1-fls.regionh.top.local')
        #     smbclient.delete_session(r'\\regionh.top.local')

        logger.info('Success:')
        logger.info(success)

        # logger.info('Starting loop')
        # # for faktura in faktQS:
        # for i, fakt in enumerate(faktQS):
        #     XML_faktura_writer = XMLFakturaWriter() 
        #     logger.info("Sending file: %s" % fakt)
        #     if not fakt.status == 10:
        #         continue
        #     x = XML_faktura_writer.create(fakt)
        #     self.writeXMLtoFile(x, str(fakt.id))
        #     # success = self.uploadToSMBShare(x)
        #     success = True
        #     if success:
        #         fakt.status = 20
        #         fakt.save()
        #     else:
        #         print('Failed up upload faktura "%s"' % str(fakt))
        #         logger.error('Failed up upload faktura "%s"' % str(fakt))

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