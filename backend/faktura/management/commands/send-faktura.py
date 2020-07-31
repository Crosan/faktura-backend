
import math
import re
from datetime import datetime

import pandas as pd
import pytz
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import now
from pytz import timezone

from backend.faktura.extra.upload.FTP_DIR import FTPDirectory
from backend.faktura.extra.xml.XML_faktura_writer import XMLFakturaWriter
from backend.faktura.models import *
from backend.faktura.models import Parsing

local_tz = pytz.timezone('Europe/Copenhagen')

class Command(BaseCommand):
    help = 'Uploads faktura answers'

    def add_arguments(self, parser):
        parser.add_argument('upload_dir', help='Indicates the directory to upload receipt messages to.')

    def handle(self, *args, **options):
        ftp = self.init_ftp()
        upload_dir = options['upload_dir'] 

        ftp_dir = FTPDirectory(upload_dir, ftp)

        parsings = self.get_unprocessed_parsings()

        xml_fakturas = self.process_parsings(parsings)

        w.run()
    
    def init_ftp(self):
        if "FTP_HOST" not in os.environ:
            print("FTP environment variables not set, exiting")
            sys.exit()

        ftp = FTP(os.environ.get('FTP_HOST'))
        ftp.login(user=os.environ.get('FTP_USER'), passwd=os.environ.get('FTP_PASSWORD'))

        return ftp
    
    def get_unprocessed_parsings(self):
        return Parsing.objects.filter(sent==False)
    
    def process_parsings(self, parsings):
        XML_faktura_writer = XMLFakturaWriter()
        return [XML_faktura_writer.create(p) for p in parsings]



class FTPHandler:

    def __init__(self, ftp_dir: FTPDirectory, xml_fakturas):
        self.ftp_dir = ftp_dir
        self.xml_fakturas
    
    def run(self):

        for f in self.xml_fakturas:
            self.ftp_dir.put_file(f)


class FTPDirectory(object):
    # regex pattern to match modified time, type and file or directory name
    pattern = r"(.*[AP]M)\s*(\S*)\s*(\S*)"

    def __init__(self, upload_dir, ftp):
        self.files = []
        self.upload_dir = upload_dir
        self.ftp = ftp

    def put_file(self, fp):
        upload_path = self.upload_dir + '/' + os.path.basename(fp.name)

        logger.info("current working dir: {}".format(self.ftp.pwd()))
        logger.info("uploading to: {}".format(upload_path))

        self.ftp.storbinary("STOR {}".format(upload_path), fp)

    def getdata(self):
        self.ftp.cwd(self.upload_dir)
        self.ftp.retrlines('LIST', self.addline)

    def addline(self, line):

        found = re.match(self.pattern, line)

        if not found:
            return

        timestamp = found.groups()[0]
        type = found.groups()[1]
        filename = found.groups()[2]

        # skipping directories as we are only interested in files
        if type == "<DIR>":
            return

        mtime = datetime.strptime(
            timestamp, "%m-%d-%y %H:%M%p") + relativedelta(hours=12)
        mtime = mtime.replace(tzinfo=local_tz)

        self.files.append((filename, mtime))
