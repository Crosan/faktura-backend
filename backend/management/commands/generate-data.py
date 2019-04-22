
from django.core.management.base import BaseCommand, CommandError
from backend.faktura.models import *
from datetime import datetime, timedelta
from django.core.management import call_command
from django.conf import settings
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now
import pytz
import pandas as pd


class Command(BaseCommand):
    help = 'Populates the database with data'

    def add_arguments(self, parser):
        parser.add_argument('-f', '--force', dest="force", action="store_true",
                            help='Override debug settings and always create dummy data.')

    def handle(self, *args, **options):

        # opret analysetyper og priser   
        #KI Priser
        KI_priser_file = settings.BASE_DIR + \
            '/backend/faktura/assets/KI eksterne priser 2018.xlsx'
            
        KI_priser_df = pd.read_excel(KI_priser_file)
        
        data_found = False
        
        for row in KI_priser_df.iterrows():   

            _, method_data = row
            
            if not data_found:
                if str(method_data[0]).lower() == "ydelseskode":
                    data_found = True
                    continue            
                continue            
            
            ydelses_kode = method_data[0]
            ydelses_navn = method_data[1]
            gruppering = method_data[2]
            kilde_navn = method_data[3]
            
            type = ""
            
            if ydelses_kode.startswith('T') or ydelses_kode.endswith('A'):
                type = "Analyse"
            else:
                type = "Blodprodukter"
            
            analyse_type = AnalyseType.objects.create(ydelses_kode=ydelses_kode, ydelses_navn=ydelses_navn, gruppering=gruppering, type=type, kilde_navn=kilde_navn)
            
            intern_pris = method_data[5]
            ekstern_pris = method_data[7]
            
            analyse_pris = AnalysePris.objects.create(intern_pris=intern_pris, ekstern_pris=ekstern_pris, analyse_type=analyse_type)
            
        #KB Priser
        KB_priser_file = settings.BASE_DIR + \
            '/backend/faktura/assets/KB eksterne priser 2018.xlsx'
            
        KB_priser_df = pd.read_excel(KB_priser_file)
        
        data_found = False
        
        for row in KB_priser_df.iterrows():   

            _, method_data = row
            
            if not data_found:
                if str(method_data[0]).lower() == "ydelseskode":
                    data_found = True
                    continue            
                continue            
            
            ydelses_kode = method_data[0]
            ydelses_navn = method_data[1]
            gruppering = method_data[2]
            kilde_navn = method_data[3]
            
            type = ""
            
            analyse_type = AnalyseType.objects.create(ydelses_kode=ydelses_kode, ydelses_navn=ydelses_navn, gruppering=gruppering, type=type, kilde_navn=kilde_navn)
            
            intern_pris = method_data[5]
            ekstern_pris = method_data[8]
            
            analyse_pris = AnalysePris.objects.create(intern_pris=intern_pris, ekstern_pris=ekstern_pris, analyse_type=analyse_type)
            
        #VTL Priser
        VTL_priser_file = settings.BASE_DIR + \
            '/backend/faktura/assets/VTL eksterne priser 2018.xlsx'
            
        VTL_priser_df = pd.read_excel(VTL_priser_file)
        
        data_found = False
        
        for row in VTL_priser_df.iterrows():   

            _, method_data = row
            
            if not data_found:
                if str(method_data[0]).lower() == "ydelseskode":
                    data_found = True
                    continue            
                continue            
            
            ydelses_kode = method_data[0]
            ydelses_navn = method_data[1]
            gruppering = method_data[2]
            kilde_navn = method_data[3]
            
            type = ""
            
            analyse_type = AnalyseType.objects.create(ydelses_kode=ydelses_kode, ydelses_navn=ydelses_navn, gruppering=gruppering, type=type, kilde_navn=kilde_navn)
            
            intern_pris = method_data[5]
            ekstern_pris = method_data[8]
            
            analyse_pris = AnalysePris.objects.create(intern_pris=intern_pris, ekstern_pris=ekstern_pris, analyse_type=analyse_type)
            
        # opret rekvirenter
        #KI Rekvirenter
        KI_rekvirenter_file = settings.BASE_DIR + \
            '/backend/faktura/assets/GLN til blodfakturering.xlsx'
            
        KI_rekvirenter_df = pd.read_excel(KI_rekvirenter_file)
        
        data_found = False
        
        for row in KI_rekvirenter_df.iterrows():
        
            _, method_data = row
            
            if not data_found:
                if str(method_data[0]).lower() == "rekv_hosp":
                    data_found = True
                    continue            
                continue 
               
            hospital = method_data[0]
            niveau = method_data[1]
            afdelingsnavn = method_data[2]
            GLN_nummer = method_data[3]
            
            rekvirent = Rekvirent.objects.create(hospital=hospital, niveau=niveau, afdelingsnavn=afdelingsnavn, GLN_nummer=GLN_nummer)
            
            
            
            
            
            
            
            
            
            
