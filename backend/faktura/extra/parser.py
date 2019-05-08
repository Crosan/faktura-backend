import pytz
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import datetime
import math

from django.core.management.base import BaseCommand, CommandError
from backend.faktura.models import *
from datetime import timedelta
from django.core.management import call_command
from django.conf import settings
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist
from backend.faktura.extra.logger import *
from django.core.files import File


class Parser:

    @classmethod
    def parse(self, parsing_object):

        excel_parser = ExcelParser()
        
        file = parsing_object.data_fil            
            
        df = pd.read_excel(file, header=None)
            
        data_source = None
            
        #Create empty list for the error data
        error_list_list = []
        
        antal_oprettet = 0
        samlet_pris = 0
            
        for row in df.iterrows():   

            _, method_data = row
                
            #Parse the data
            #If the data source if blodbank
            if data_source and data_source.lower() == "blodbank":
                #Parse row and save result
                analyse = excel_parser.parse_blodbank(method_data, parsing_object)
                #If there was an error append the data to error list
                if not analyse:
                    error_list_list.append(method_data)
                else:
                    antal_oprettet = antal_oprettet + 1
                    samlet_pris = samlet_pris + analyse.pris
            #If the data source is LABKA
            elif data_source and data_source.lower() == "labka":
                #Parse row and save result
                analyse = excel_parser.parse_labka(method_data, parsing_object)
                #If there was an error append the data to error list
                if not analyse:
                    error_list_list.append(method_data)
                else:
                    antal_oprettet = antal_oprettet + 1
                    samlet_pris = samlet_pris + analyse.pris
                
            #Set data source
            if not data_source and str(method_data[0]).lower() == "antal":
                data_source = "blodbank"
                #Set headers for error data
                error_list_list.append(method_data)
            elif not data_source:
                data_source = "labka"
                #Set headers for error data
                error_list_list.append(method_data)
                
        #Create data frame from error data
        error_list_df = pd.DataFrame(error_list_list)
        
        #Write to excel
        mangel_liste_file_path = './media/mangellister/{}.xlsx'.format(parsing_object.id)
        writer = ExcelWriter(mangel_liste_file_path)
        error_list_df.to_excel(writer, 'Mangelliste', index=False, header=None)
        writer.save()
        
        parsing_object.mangel_liste_fil = 'mangellister/{}.xlsx'.format(parsing_object.id)
        parsing_object.antal_oprettet = antal_oprettet
        parsing_object.samlet_pris = samlet_pris


class ExcelParser:
    def get_blodbank_rekvirent(self, HOSPITAL, L4NAME, L6NAME, analyse_type):
        rekvirent = None
    
        if HOSPITAL == 'Bispebjerg og Frederiksberg Hospitaler':
            try:
                rekvirent = Rekvirent.objects.get(hospital=HOSPITAL, niveau='L6Name', afdelingsnavn=L6NAME)
            except ObjectDoesNotExist:
                try:
                    rekvirent = Rekvirent.objects.get(hospital=HOSPITAL, niveau='L4Name', afdelingsnavn=L4NAME)
                except ObjectDoesNotExist:
                    Logger.log("Fejl - Kunne ikke finde rekvirent " + HOSPITAL + " - " + L4NAME + " - " + L6NAME)
                    
        elif HOSPITAL == 'Bornholm':
            if not analyse_type.type == "Analyse":
                Logger.log("Fejl - Bornholm skal kun afregnes for virusanalyser")
                return None
        
            rekvirent = Rekvirent.objects.get(hospital=HOSPITAL)
            
        elif HOSPITAL == 'Amager og Hvidovre Hospital':
            try:
                rekvirent = Rekvirent.objects.get(hospital=HOSPITAL, niveau='L6Name', afdelingsnavn=L6NAME)
            except ObjectDoesNotExist:
                try:
                    rekvirent = Rekvirent.objects.get(hospital=HOSPITAL, niveau='L4Name', afdelingsnavn=L4NAME)
                except ObjectDoesNotExist:
                    Logger.log("Fejl - Kunne ikke finde rekvirent " + HOSPITAL + " - " + L4NAME + " - " + L6NAME)
            
        elif HOSPITAL == 'Herlev og Gentofte Hospital':
            try:
                rekvirent = Rekvirent.objects.get(hospital=HOSPITAL, niveau='L4Name', afdelingsnavn=L4NAME)
            except ObjectDoesNotExist:
                Logger.log("Fejl - Kunne ikke finde rekvirent " + HOSPITAL + " - " + L4NAME + " - " + L6NAME)
            
            if rekvirent and rekvirent.GLN_nummer == "5798001502092":
                if not analyse_type.type == "Blodprodukt":
                    Logger.log("Fejl - Hud- og allergiafdeling, overafd. U, GE skal kun afregnes for blodprodukter")
                    return None
            
        elif HOSPITAL == 'Rigshospitalet' and L4NAME == 'Medicinsk overafd., M GLO':
            rekvirent = Rekvirent.objects.get(GLN_nummer="5798001026031")
            
        elif HOSPITAL == 'Hospitalerne i Nordsjælland':
            rekvirent = Rekvirent.objects.get(GLN_nummer="5798001068154")
            
        else:
            Logger.log("Fejl - Kunne ikke finde rekvirent " + HOSPITAL + " - " + L4NAME + " - " + L6NAME)
            
        return rekvirent
        
    
    def parse_blodbank(self, method_data, parsing_object):
        ANTAL = method_data[0]
        YDELSESKODE = method_data[1]
        HOSPITAL = method_data[12]
        L4NAME = method_data[14]
        L6NAME = method_data[17]
        #Maybe try/catch here
        SVAR_DATO = datetime.strptime(method_data[19], "%Y%m%d").replace(tzinfo=pytz.UTC)
        INSERT_DATO = method_data[20]
        CPR = method_data[21]
        
        analyse_type = None
        
        try:
            analyse_type = AnalyseType.objects.get(ydelses_kode=YDELSESKODE)
        except ObjectDoesNotExist:
            Logger.log("Fejl - Kunne ikke finde analyse med ydelseskode " + YDELSESKODE) 

        rekvirent = self.get_blodbank_rekvirent(str(HOSPITAL), str(L4NAME), str(L6NAME), analyse_type)
            
        PRIS = ""
            
        if analyse_type and rekvirent:
        
            if math.isnan(ANTAL):
                Logger.log("Fejl - Antallet af analyser ikke angivet for analyse med ydelseskode " + YDELSESKODE)
                return None
            
            for p in analyse_type.priser.order_by('-gyldig_fra'):
                if p.gyldig_fra < now() and (not p.gyldig_til or p.gyldig_til > now()):
                    PRIS = p.ekstern_pris
                    
            analyse = Analyse.objects.create(antal=ANTAL, pris=PRIS, CPR=CPR, svar_dato=SVAR_DATO, analyse_type=analyse_type, rekvirent=rekvirent, parsing=parsing_object)
            
            print(analyse)
            return analyse
            
        return None
        
    def get_labka_rekvirent(self, REKVIRENT, PAYERCODE, EAN_NUMMER, analyse_type):
        rekvirent = None
        
        try:
            rekvirent = Rekvirent.objects.get(hospital=REKVIRENT, afdelingsnavn=PAYERCODE, GLN_nummer=EAN_NUMMER)
        except ObjectDoesNotExist:
            rekvirent = Rekvirent.objects.create(hospital=REKVIRENT, afdelingsnavn=PAYERCODE, GLN_nummer=EAN_NUMMER)
            
        return rekvirent
        
    def parse_labka(self, method_data, parsing_object):
        ANTAL = 1
        CPR = method_data[3]
        YDELSESKODE = method_data[4]
        #Maybe try/catch here
        SVAR_DATO = method_data[10].replace(tzinfo=pytz.UTC)
        REKVIRENT = method_data[13]
        PAYERCODE = method_data[14]
        EAN_NUMMER = method_data[21]
        
        if not str(EAN_NUMMER):
            Logger.log("Fejl - Intet EAN_nummer angivet")
            return None
        
        analyse_type = None

        try:
            analyse_type = AnalyseType.objects.get(ydelses_kode=YDELSESKODE)
        except ObjectDoesNotExist:
            Logger.log("Fejl - Kunne ikke finde analyse med ydelseskode " + YDELSESKODE) 

        rekvirent = self.get_labka_rekvirent(str(REKVIRENT), str(PAYERCODE), str(EAN_NUMMER), analyse_type)
            
        PRIS = ""
            
        if analyse_type and rekvirent:
        
            if math.isnan(ANTAL):
                Logger.log("Fejl - Antallet af analyser ikke angivet for analyse med ydelseskode " + YDELSESKODE)
                return None
            
            for p in analyse_type.priser.order_by('-gyldig_fra'):
                if p.gyldig_fra < now() and (not p.gyldig_til or p.gyldig_til > now()):
                    PRIS = p.ekstern_pris
                    
            analyse = Analyse.objects.create(antal=ANTAL, pris=PRIS, CPR=CPR, svar_dato=SVAR_DATO, analyse_type=analyse_type, rekvirent=rekvirent, parsing=parsing_object)
            
            print(analyse)
            return analyse
            
        return None
