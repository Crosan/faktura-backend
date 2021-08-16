import logging
import math
import re
from datetime import datetime
import time

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
    serverLocation = os.path.join(settings.SMB_MOUNT_POINT, settings.SMB_PATH)
    logger.info('Serverlocation is: ' + serverLocation)
    # else:
    #     serverLocation = r"\\regionh.top.local\DFS\Systemer\SAP\SAP001\DIAC2SAP\Prod\ "


    def writeXMLtoFile(self, xml, filename):
        ''' For testing/debugging purposes '''
        filename += '.xml'
        outpath = os.path.join(os.getcwd(), 'backend', 'media', 'xml_output', filename)
        logger.info('Writing xml file to: %s' % outpath)

        with open(outpath, 'w', encoding='utf-8') as f:
            f.write(xml)
    
    def uploadToSMBShare(self, content) -> str:
        ''' Uses the server location from the class namespace and generates a timestamped filename

        Parameters:
            content : XML-formatted text 
            
        Returns:
            The faktura filename'''
        filename = r'DIAFaktura_' + datetime.now().strftime("%Y%m%d_%H%M%S%f")[:-4] + '.xml'
        logger.info('Output filename is: ' + filename)
        dst = os.path.join(self.serverLocation, filename)
        logger.info('Sending faktura to: %s' % dst)

        try:
            with open(dst, 'w', encoding='utf-8') as f:
                f.write(content)
        except:
            logger.error("Unexpected error:" + str(sys.exc_info()[0]))
        finally:
            return filename

    def handle(self, *args, **options):
        logger.info(str(options))

        debitor = options['settings'].get('debitor', None)
        parse = options['settings'].get('parsing', None)

        if not debitor:
            logger.error('Sendfaktura called with no debitor ID')
            return 

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
        excludeDict = {
                'Hovedstaden': Q(analyse_type__regionh=True),
                'Sjælland': Q(analyse_type__sjaelland=True),
                'Syddanmark': Q(analyse_type__syddanmark=True),
                'Nordjylland': Q(analyse_type__nordjylland=True),
                'Midtjylland': Q(analyse_type__midtjylland=True)
            }
        excludeQ = excludeDict.get(chosenDebitor.region, None)

        analQS = Analyse.objects.filter(
                faktura__rekvirent__debitor__id=int(debitor)
            ).filter(
                faktura__parsing__id=int(parse)
            ).filter(
                faktura__status=10
            # ).filter(
            #     excludeQ
            )

        if chosenDebitor.region:
            analQS = analQS.filter(excludeQ)
        
        logger.info(chosenDebitor)
        logger.info("Antal analyser: %d" % len(analQS))

        logger.info('Starting writing the faktura')
        XML_faktura_writer = XMLFakturaWriter()

        try:
            output = XML_faktura_writer.create(chosenDebitor, analQS)
            self.writeXMLtoFile(output, parse + '_' +  chosenDebitor.debitor_nr, faktQS[0].id)
            filename = self.uploadToSMBShare(output)
            for faktura in faktQS:
                faktura.status = 20
                faktura.save()
            success = True
            logger.info('Running listdir')
            dirlisting = os.listdir(self.serverLocation)
            logger.info(dirlisting)
            success = filename in dirlisting
        except:
            logger.error('Writing or uploading xml file failed')
            success = False

        logger.info('Success:' + str(success))
        return