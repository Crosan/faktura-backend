
from django.core.management.base import BaseCommand, CommandError
from backend.backend.models import *
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
        analyse_typer_og_priser_filename = settings.BASE_DIR + \
            '/backend/backend/assets/KI_eksterne_priser_2018.csv'

        analyse_typer_og_priser_data_frame = pd.read_csv(
            analyse_typer_og_priser_filename, sep=';', encoding='latin-1')
        
        for row in analyse_typer_og_priser_data_frame.iterrows():
        
            _, method_data = row
             
            ydelses_kode = method_data[0]
            ydelses_navn = method_data[1]
            gruppering = method_data[2]
            kilde_navn = method_data[3]
            
            type = ""
            
            if ydelses_kode.startswith('A') or ydelses_kode.endswith('T'):
                type = "Analyse"
            else:
                type = "Blodprodukter"
            
            analyse_type = AnalyseType.objects.create(ydelses_kode=ydelses_kode, ydelses_navn=ydelses_navn, gruppering=gruppering, type=type, kilde_navn=kilde_navn)
            
            intern_pris = method_data[5]
            ekstern_pris = method_data[7]
            
            analyse_pris = AnalysePris.objects.create(intern_pris=intern_pris, ekstern_pris=ekstern_pris, analyse_type=analyse_type)
            
        # opret rekvirenter
        rekvirenter_filename = settings.BASE_DIR + \
            '/backend/backend/assets/GLN_til_blodfakturering.csv'

        rekvirenter_frame = pd.read_csv(
            rekvirenter_filename, sep=';', encoding='latin-1')  
           
        for row in rekvirenter_frame.iterrows():
            
            _, method_data = row
             
            hospital = method_data[0]
            niveau = method_data[1]
            afdelingsnavn = method_data[2]
            GLN_nummer = method_data[3]
            
            rekvirent = Rekvirent.objects.create(hospital=hospital, niveau=niveau, afdelingsnavn=afdelingsnavn, GLN_nummer=GLN_nummer)
            
            
            
            
            
            
            
            
            
            
