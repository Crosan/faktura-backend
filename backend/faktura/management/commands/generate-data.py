
from django.core.management.base import BaseCommand, CommandError
from backend.faktura.models import *
from django.core.management import call_command
from django.conf import settings
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now
import pandas as pd
import math
import pytz
from pytz import timezone
from datetime import datetime


class Command(BaseCommand):
    help = 'Populates the database with data'

    def add_arguments(self, parser):
        parser.add_argument('-f', '--force', dest="force", action="store_true",
                            help='Override debug settings and always create dummy data.')
    

    def handle(self, *args, **options):
    
        #Convert datetime
        def to_UTC(self, d : datetime):
            cph_tz = timezone('Europe/Copenhagen')
            return cph_tz.normalize(cph_tz.localize(d)).astimezone(pytz.utc)
    
        #Creates an analyse_type object
        def create_analyse_type(method_data):
        
            ydelses_kode = method_data[0]
            ydelses_navn = method_data[1]
            gruppering = method_data[2]
            kilde_navn = method_data[3]
            afdeling = method_data[6]
            
            if not isinstance(gruppering, str):
                gruppering = ""
                
            if not isinstance(kilde_navn, str):
                kilde_navn = ""
            
            type = ""
            
            if afdeling == "KI":
                if ydelses_kode.startswith('T') or ydelses_kode.endswith('A'):
                    type = "Analyse"
                else:
                    type = "Blodprodukt"
                    
            try:
                analyse_type = AnalyseType.objects.get(ydelses_kode=method_data[0])   
            except:
                analyse_type = AnalyseType.objects.create(ydelses_kode=ydelses_kode, ydelses_navn=ydelses_navn, gruppering=gruppering, afdeling=afdeling, type=type, kilde_navn=kilde_navn)
            
            return analyse_type
            
        #Creates an analyse_pris object
        def create_analyse_pris(method_data):
            
            intern_pris = method_data[4]
            ekstern_pris = method_data[5]
            try:
                gyldig_fra = to_UTC(method_data[7])
            except:
                gyldig_fra = now()
                
            try:
                gyldig_til = to_UTC(method_data[8])
            except:
                gyldig_til = None
                
            analyse_pris = AnalysePris.objects.create(intern_pris=intern_pris, ekstern_pris=ekstern_pris, gyldig_fra=gyldig_fra, gyldig_til=gyldig_til, analyse_type=analyse_type)              
                
            return analyse_pris    

        # opret analysetyper og priser   
        #KI Priser
        print("Creating KI analyse_type and analyse_pris objects...")
        
        KI_priser_file = settings.BASE_DIR + \
            '/backend/faktura/assets/KI eksterne priser 2018.xlsx'
            
        KI_priser_df = pd.read_excel(KI_priser_file, header=None)
        
        data_found = False
        
        for row in KI_priser_df.iterrows():  

            _, method_data = row
            
            if not data_found:
                if str(method_data[0]).lower() == "ydelseskode":
                    data_found = True
                    continue            
                continue         
            
            analyse_type = create_analyse_type(method_data)
            
            analyse_pris = create_analyse_pris(method_data)
            
            
        #KB Priser
        print("Creating KB analyse_type and analyse_pris objects...")
        
        KB_priser_file = settings.BASE_DIR + \
            '/backend/faktura/assets/KB eksterne priser 2018.xlsx'
            
        KB_priser_df = pd.read_excel(KB_priser_file, header=None)
        
        data_found = False
        
        for row in KB_priser_df.iterrows():   

            _, method_data = row
            
            if not data_found:
                if str(method_data[0]).lower() == "ydelseskode":
                    data_found = True
                    continue            
                continue         
            
            analyse_type = create_analyse_type(method_data)
            
            analyse_pris = create_analyse_pris(method_data)
            
        #VTL Priser
        print("Creating VTL analyse_type and analyse_pris objects...")
        
        VTL_priser_file = settings.BASE_DIR + \
            '/backend/faktura/assets/VTL eksterne priser 2018.xlsx'
            
        VTL_priser_df = pd.read_excel(VTL_priser_file, header=None)
        
        data_found = False
        
        for row in VTL_priser_df.iterrows():   

            _, method_data = row
            
            if not data_found:
                if str(method_data[0]).lower() == "ydelseskode":
                    data_found = True
                    continue            
                continue         
            
            analyse_type = create_analyse_type(method_data)
            
            analyse_pris = create_analyse_pris(method_data)
            
        #GM Priser
        print("Creating GM analyse_type and analyse_pris objects...")
        
        GM_priser_file = settings.BASE_DIR + \
            '/backend/faktura/assets/GM eksterne priser 2018.xlsx'
            
        GM_priser_df = pd.read_excel(GM_priser_file, header=None)
        
        data_found = False
        
        for row in GM_priser_df.iterrows():   

            _, method_data = row
            
            if not data_found:
                if str(method_data[0]).lower() == "ydelseskode":
                    data_found = True
                    continue            
                continue         
            
            analyse_type = create_analyse_type(method_data)
            
            analyse_pris = create_analyse_pris(method_data)
            
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
            
            
            
            
            
            
            
            
            
            
