
from django.core.management.base import BaseCommand, CommandError
from backend.faktura.models import *
from datetime import timedelta
from django.core.management import call_command
from django.conf import settings
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist
import pytz
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import datetime
import math
import logging

logger = logging.getLogger("app")

from backend.faktura.extra.parser import Parser


class Command(BaseCommand):
    help = 'Populates the database with dummy data'

    def add_arguments(self, parser):
        parser.add_argument('--file', dest="file_path", required=False,
                            help='Path to excel file to parse (used for testing purposes).')
    
        
    def handle(self, *args, **options):
        parser = Parser()
        parser.parse(None, options["file_path"])
    
        # def get_blodbank_rekvirent(HOSPITAL, L4NAME, L6NAME, analyse_type):
        #     rekvirent = None
        
        #     if HOSPITAL == 'Bispebjerg og Frederiksberg Hospitaler':
        #         try:
        #             rekvirent = Rekvirent.objects.get(hospital=HOSPITAL, niveau='L6Name', afdelingsnavn=L6NAME)
        #         except ObjectDoesNotExist:
        #             try:
        #                 rekvirent = Rekvirent.objects.get(hospital=HOSPITAL, niveau='L4Name', afdelingsnavn=L4NAME)
        #             except ObjectDoesNotExist:
        #                 logger.log("Fejl - Kunne ikke finde rekvirent " + HOSPITAL + " - " + L4NAME + " - " + L6NAME)
                        
        #     elif HOSPITAL == 'Bornholm':
        #         if not analyse_type.type == "Analyse":
        #             logger.log("Fejl - Bornholm skal kun afregnes for virusanalyser")
        #             return None
            
        #         rekvirent = Rekvirent.objects.get(hospital=HOSPITAL)
                
        #     elif HOSPITAL == 'Amager og Hvidovre Hospital':
        #         try:
        #             rekvirent = Rekvirent.objects.get(hospital=HOSPITAL, niveau='L6Name', afdelingsnavn=L6NAME)
        #         except ObjectDoesNotExist:
        #             try:
        #                 rekvirent = Rekvirent.objects.get(hospital=HOSPITAL, niveau='L4Name', afdelingsnavn=L4NAME)
        #             except ObjectDoesNotExist:
        #                 logger.log("Fejl - Kunne ikke finde rekvirent " + HOSPITAL + " - " + L4NAME + " - " + L6NAME)
                
        #     elif HOSPITAL == 'Herlev og Gentofte Hospital':
        #         try:
        #             rekvirent = Rekvirent.objects.get(hospital=HOSPITAL, niveau='L4Name', afdelingsnavn=L4NAME)
        #         except ObjectDoesNotExist:
        #             logger.log("Fejl - Kunne ikke finde rekvirent " + HOSPITAL + " - " + L4NAME + " - " + L6NAME)
                
        #         if rekvirent and rekvirent.GLN_nummer == "5798001502092":
        #             if not analyse_type.type == "Blodprodukt":
        #                 logger.log("Fejl - Hud- og allergiafdeling, overafd. U, GE skal kun afregnes for blodprodukter")
        #                 return None
                
        #     elif HOSPITAL == 'Rigshospitalet' and L4NAME == 'Medicinsk overafd., M GLO':
        #         rekvirent = Rekvirent.objects.get(GLN_nummer="5798001026031")
                
        #     elif HOSPITAL == 'Hospitalerne i Nordsjælland':
        #         rekvirent = Rekvirent.objects.get(GLN_nummer="5798001068154")
                
        #     else:
        #         logger.log("Fejl - Kunne ikke finde rekvirent " + HOSPITAL + " - " + L4NAME + " - " + L6NAME)
                
        #     return rekvirent
            
    
        # def parse_blodbank(method_data):
        #     ANTAL = method_data[0]
        #     YDELSESKODE = method_data[1]
        #     HOSPITAL = method_data[12]
        #     L4NAME = method_data[14]
        #     L6NAME = method_data[17]
        #     #Maybe try/catch here
        #     SVAR_DATO = datetime.datetime.strptime(method_data[19], "%Y%m%d").replace(tzinfo=pytz.UTC)
        #     INSERT_DATO = method_data[20]
        #     CPR = method_data[21]
            
        #     analyse_type = None
            
        #     try:
        #         analyse_type = AnalyseType.objects.get(ydelses_kode=YDELSESKODE)
        #     except ObjectDoesNotExist:
        #         logger.log("Fejl - Kunne ikke finde analyse med ydelseskode " + YDELSESKODE) 

        #     rekvirent = get_blodbank_rekvirent(str(HOSPITAL), str(L4NAME), str(L6NAME), analyse_type)
                
        #     PRIS = ""
                
        #     if analyse_type and rekvirent:
            
        #         if math.isnan(ANTAL):
        #             logger.log("Fejl - Antallet af analyser ikke angivet for analyse med ydelseskode " + YDELSESKODE)
        #             return False
                
        #         for p in analyse_type.priser.order_by('-gyldig_fra'):
        #             if p.gyldig_fra < now() and (not p.gyldig_til or p.gyldig_til > now()):
        #                 PRIS = p.ekstern_pris
                        
        #         analyse = Analyse.objects.create(antal=ANTAL, pris=PRIS, CPR=CPR, svar_dato=SVAR_DATO, analyse_type=analyse_type, rekvirent=rekvirent)
                
        #         print(analyse)
        #         return True
                
        #     return False
            
        # def get_labka_rekvirent(HOSPITAL, AFDELING, EAN_NUMMER, analyse_type):
        #     rekvirent = None
            
        #     try:
        #         rekvirent = Rekvirent.objects.get(hospital=HOSPITAL, afdelingsnavn=AFDELING, GLN_nummer=EAN_NUMMER)
        #     except ObjectDoesNotExist:
        #         rekvirent = Rekvirent.objects.create(hospital=HOSPITAL, afdelingsnavn=AFDELING, GLN_nummer=EAN_NUMMER)
                
        #     return rekvirent
            
        # def parse_labka(method_data):
        #     ANTAL = 1
        #     CPR = method_data[3]
        #     YDELSESKODE = method_data[4]
        #     #Maybe try/catch here
        #     SVAR_DATO = method_data[10].replace(tzinfo=pytz.UTC)
        #     AFDELING = method_data[13]
        #     HOSPITAL = method_data[20]
        #     EAN_NUMMER = method_data[21]
            
        #     if not str(EAN_NUMMER):
        #         logger.log("Fejl - Intet EAN_nummer angivet")
        #         return False
            
        #     analyse_type = None

        #     try:
        #         analyse_type = AnalyseType.objects.get(ydelses_kode=YDELSESKODE)
        #     except ObjectDoesNotExist:
        #         logger.log("Fejl - Kunne ikke finde analyse med ydelseskode " + YDELSESKODE) 

        #     rekvirent = get_labka_rekvirent(str(HOSPITAL), str(AFDELING), str(EAN_NUMMER), analyse_type)
                
        #     PRIS = ""
                
        #     if analyse_type and rekvirent:
            
        #         if math.isnan(ANTAL):
        #             logger.log("Fejl - Antallet af analyser ikke angivet for analyse med ydelseskode " + YDELSESKODE)
        #             return False
                
        #         for p in analyse_type.priser.order_by('-gyldig_fra'):
        #             if p.gyldig_fra < now() and (not p.gyldig_til or p.gyldig_til > now()):
        #                 PRIS = p.ekstern_pris
                        
        #         analyse = Analyse.objects.create(antal=ANTAL, pris=PRIS, CPR=CPR, svar_dato=SVAR_DATO, analyse_type=analyse_type, rekvirent=rekvirent)
                
        #         print(analyse)
        #         return True
                
        #     return False
    
        # if options['file_path']:
        #     KI_priser_file = options['file_path']            
            
        #     KI_priser_df = pd.read_excel(KI_priser_file, header=None)
            
        #     data_source = None
            
        #     #Create empty list for the error data
        #     error_list_list = []
            
        #     for row in KI_priser_df.iterrows():   

        #         _, method_data = row
                
        #         #Parse the data
        #         if data_source and data_source.lower() == "blodbank":
        #             #If there was an error append the data
        #             if not parse_blodbank(method_data):
        #                 error_list_list.append(method_data)
        #         elif data_source and data_source.lower() == "labka":
        #             if not parse_labka(method_data):
        #                 error_list_list.append(method_data)
                
        #         #Set data source
        #         if not data_source and str(method_data[0]).lower() == "antal":
        #             data_source = "blodbank"
        #             #Set headers for error data
        #             error_list_list.append(method_data)
        #         elif not data_source:
        #             data_source = "labka"
        #             #Set headers for error data
        #             error_list_list.append(method_data)
                
        #     #Create data frame from error data
        #     error_list_df = pd.DataFrame(error_list_list)
            
        #     #Write to excel
        #     writer = ExcelWriter('Pandas-Example2.xlsx')
        #     error_list_df.to_excel(writer, 'Mangelliste', index=False, header=None)
        #     writer.save()
            
        # else:
        #     print("HEY")   
    
        
