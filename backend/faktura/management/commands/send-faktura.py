import logging
import math
import re
from datetime import datetime

from smb.SMBConnection import SMBConnection
from smb.smb_structs import OperationFailure

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
from backend.faktura.models import Parsing
from ftplib import FTP, error_perm

logger = logging.getLogger(__name__)
local_tz = pytz.timezone('Europe/Copenhagen')

class Command(BaseCommand):
    help = 'Uploads faktura answers'

    def handle(self, *args, **options):
        self.print_env()

        try:
            conn = self.test_smb_conn()
        except:
            return
            None

        conn.connect(os.environ.get('FTP_HOST'), 445)

        print("login successful")

        parsings = self.get_unprocessed_parsings()

        xml_fakturas = self.process_parsings(parsings)

        django_xml_fakturas = self.generate_django_xml_fakturas(xml_fakturas)

        print("prepared fakturas")

        ## Overvej her at slette successfuldt sendte fakturaer da de kan fylde ganske meget

        upload_dir = os.environ.get('FTP_UPLOAD_DIR')
        worker = Worker(conn, upload_dir, django_xml_fakturas)

        worker.run()

    def setup_smb_conn(self):
        conn=SMBConnection(os.environ.get('FTP_USER'),os.environ.get('FTP_PASSWORD'),"","",use_ntlm_v2 = True)
        return conn


    def print_env(self):
        logger.info("HOST: {}\nUSER: {}\nUPLOAD_DIR: {}".format(os.environ.get('FTP_HOST'), os.environ.get('FTP_USER'), os.environ.get('FTP_UPLOAD_DIR')))
    
    def get_unprocessed_parsings(self):
        return Parsing.objects.filter(sent=False)
    
    def process_parsings(self, parsings):
        XML_faktura_writer = XMLFakturaWriter()
        return [XML_faktura_writer.create(p) for p in parsings]

    def generate_django_xml_fakturas(self, xml_fakturas):
        res = []
        for f in xml_fakturas:
            django_xml_faktura = FakturaXml.objects.create()
            django_xml_faktura.file.save("xml", ContentFile(f))
            res.append(django_xml_faktura)

        return res

    # def init_ftp(self):
    #     if "FTP_HOST" not in os.environ:
    #         print("FTP environment variables not set, exiting")
    #         sys.exit()

    #     ftp = FTP(os.environ.get('FTP_HOST'))
    #     ftp.login(user=os.environ.get('FTP_USER'), passwd=os.environ.get('FTP_PASSWORD'))

    #     return ftp

class Worker:

    def __init__(self, smb_conn: SMBConnection, upload_dir, xml_fakturas):
        self.smb_conn = smb_conn
        self.upload_dir = upload_dir
        self.xml_fakturas
    
    def run(self):
        for f in self.xml_fakturas:
            try:
                self.smb_conn.storeFile(self.upload_dir, os.path.basename(f.file.name), f.file)
            except OperationFailure as e:
                print(e)

            # remove this just for testing to see if one file gets uploaded
            return


# class FTPDirectory(object):
    # # regex pattern to match modified time, type and file or directory name
    # pattern = r"(.*[AP]M)\s*(\S*)\s*(\S*)"

    # def __init__(self, upload_dir, ftp):
    #     self.files = []
    #     self.upload_dir = upload_dir
    #     self.ftp = ftp

    # def put_file(self, fp):
    #     upload_path = self.upload_dir + '/' + os.path.basename(fp.name)

    #     logger.info("current working dir: {}".format(self.ftp.pwd()))
    #     logger.info("uploading to: {}".format(upload_path))

    #     self.ftp.storbinary("STOR {}".format(upload_path), fp)

    # def getdata(self):
    #     self.ftp.cwd(self.upload_dir)
    #     self.ftp.retrlines('LIST', self.addline)

    # def addline(self, line):

    #     found = re.match(self.pattern, line)

    #     if not found:
    #         return

    #     timestamp = found.groups()[0]
    #     type = found.groups()[1]
    #     filename = found.groups()[2]

    #     # skipping directories as we are only interested in files
    #     if type == "<DIR>":
    #         return

    #     mtime = datetime.strptime(
    #         timestamp, "%m-%d-%y %H:%M%p") + relativedelta(hours=12)
    #     mtime = mtime.replace(tzinfo=local_tz)

    #     self.files.append((filename, mtime))
