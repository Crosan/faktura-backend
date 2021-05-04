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

import smbclient


logger = logging.getLogger(__name__)
local_tz = pytz.timezone('Europe/Copenhagen')

class Command(BaseCommand):
    help = 'Uploads faktura answers'

    def handle(self, *args, **options):
        # self.print_env()


        # Optional - specify the default credentials to use on the global config object
        # smbclient.ClientConfig(username='user', password='pass')

        # Optional - register the credentials with a server (overrides ClientConfig for that server)
        smbclient.register_session(r"regionh.top.local", username="***REMOVED***", password="***REMOVED***")
        # print(smbclient.listdir(r"\\regionh.top.local\DFS\Systemer\SAP\SAP001"))#\DIAC2SAP\Prod\"))
        print(smbclient.listdir(r"\\regionh.top.local\DFS\Systemer\SAP\SAP001\DIAC2SAP\Test"))#\DIAC2SAP\Prod\"))
        # print(smbclient.stat('regionh.top.local\\DFS\\Systemer\\SAP\\SAP002\\beholdnings_styring\\prd\\backup\\DQ10053790-08.02.2021-08.19.04.csv'))

        # smbclient.mkdir(r"\\server\share\directory", username="user", password="pass")

        # with smbclient.open_file(r"\\server\share\directory\file.txt", mode="w") as fd:
        #     fd.write(u"file contents")

        # try:
        #     conn = self.setup_smb_conn()
        # except:
        #     print("failed connect")

        #     return None

        # conn.connect('//regionh.top.local/DFS/', 445)

        # print("login successful")


        # upload_dir = os.environ.get('FTP_UPLOAD_DIR')
        # worker = Worker(conn, upload_dir, django_xml_fakturas)

        # worker.run()

        # /\regionh.top.local\DFS\Systemer\SAP\SAP002\beholdnings_styring\prd\backup\DQ10053790-08.02.2021-08.19.04.csv



    # def setup_smb_conn(self):
    #     pswd0 = r"***REMOVED***"
    #     pswd1 = r"***REMOVED***"
    #     conn = SMBConnection(,"","",use_ntlm_v2 = True)
    #     return conn
# SMBConnection(username, password, my_name, remote_name, domain='', use_ntlm_v2=True, sign_options=2, is_direct_tcp=False)

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
