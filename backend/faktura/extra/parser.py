import pytz
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import datetime
import math
import time
import sys

from django.core.management.base import BaseCommand, CommandError
from backend.faktura.models import *
from datetime import timedelta, datetime
from django.core.management import call_command
from django.conf import settings
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now, make_aware
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File

import logging

logger = logging.getLogger("app")


class NewParser:
    def __init__(cls):
        print('New parser initialised')

    @classmethod
    def parseLabka(cls, parsing_object=None, file_path=None, metatype='Labka'):
        print("Begin parsing '%s'" % file_path)

        # if not file_path:
        #     file = parsing_object.data_fil
        # else:
        #     file = file_path

        current_parsing = Parsing.objects.create(
            data_fil=file_path, ptype=metatype)

        mangel_liste_file_name = os.path.splitext(os.path.basename(file_path))[
            0] + '_Mangel_' + str(current_parsing.id) + '.xlsx'
        mangel_liste_file_path = os.path.join(
            os.getcwd(), 'backend', 'media', 'mangellister', mangel_liste_file_name)

        current_parsing.mangel_liste_fil = mangel_liste_file_path
        current_parsing.save()

        # NOTE: Husk at rownr i errors er off by 2 i forhold til original xlsx!
        error_lines = []  # Indexes of rows in input file that have failed

        known_analyse_typer = {}  # Not used as of now
        # known_analyse_typer = {
        #     "Labkakode" : AnalyseID
        # }

        known_rekvirent_names = {}
        # known_rekvirent_names = {
        #     "Rekvirent Name" : RekvirentID,
        # }

        known_fakturaer = {}
        # known_fakturaer = {
        #     RekvirentID : FaktID,
        # }

        desired_cols = ["BETALERGRUPPE_SOR",
                        "CPRNR",
                        "LABKAKODE",
                        "EKSTERN_PRIS",
                        "REKVIRENT",
                        "SHORTNME",
                        "EAN_NUMMER",
                        "PRVTAGNDATO",
                        "SVARDATO"]

        print("Loading file into memory...")

        df = pd.read_excel(file_path, header=0, usecols=desired_cols)
        total_rows = len(df)

        GLN_file = settings.BASE_DIR + '/faktura/assets/patoweb/GLN.xlsx'
        kommune_file = settings.BASE_DIR + '/faktura/assets/patoweb/kommune.xlsx'
        GLN = pd.read_excel(GLN_file)
        kommune = pd.read_excel(kommune_file)

        # Loop through all lines in input xlsx file
        print('Starting loop')
        time_left = 0
        t0 = time.perf_counter()
        for row in df.iterrows():

            rownr, rowdata = row

            # Calculate remaining time
            if (rownr % 100 == 0) and (rownr > 2000):
                time_passed = time.perf_counter() - t0
                time_pr_row = time_passed / (rownr + 1)
                time_left   = timedelta(seconds = int((total_rows - rownr + 1) * time_pr_row))

            sys.stdout.write('\r%d / %d %s' % (rownr+1, total_rows, "" if time_left == 0 else "(%s remaining)" % (time_left)))

            # Store all fields in temporary variables
            r_betalergruppe = cls.__cleanValues(rowdata['BETALERGRUPPE_SOR'])
            r_cprnr         = rowdata['CPRNR']
            r_labkakode     = rowdata['LABKAKODE']
            r_ekstern_pris  = rowdata['EKSTERN_PRIS']
            r_rekvirent     = cls.__cleanValues(rowdata['REKVIRENT'])
            r_shortname     = cls.__cleanValues(rowdata['SHORTNME'])#.strip()
            r_ean_nummer    = cls.__cleanValues(rowdata['EAN_NUMMER'])
            r_prvdato       = make_aware(rowdata['PRVTAGNDATO'])
            r_svardato      = make_aware(rowdata['SVARDATO'])

            # print(r_betalergruppe, r_cprnr, r_labkakode, r_ekstern_pris,  r_rekvirent, r_shortname, r_ean_nummer)

            # Find analysetype
            if r_labkakode in known_analyse_typer.keys():
                analyse_type_id = known_analyse_typer[r_labkakode]
            else:
                analyse_type_id = cls.__find_analyse_type_id(r_labkakode)
                known_analyse_typer[r_labkakode] = analyse_type_id

            # Check that analysetype exists
            if not analyse_type_id:
                error_lines.append(
                    # (rownr, 'Analyse type "%s" kendes ikke' % r_labkakode))
                    rownr)
                continue

            betalergruppe_id = cls.__find_or_create_betalergruppe(
                r_betalergruppe, metatype) if r_betalergruppe else None

            # Check that betalergruppe is specified #Maybe do this later?
            # if pd.isnull(r_betalergruppe) or (not betalergruppe_id):
            #     print('Null betalergruppe' + str(rownr))
            #     error_lines.append((rownr, 'Betalergruppe ikke udfyldt'))
            #     continue

            # Check if we have already seen this rekvirent during this parsing,
            # and consequently also know the faktura ID
            if r_rekvirent in known_rekvirent_names.keys():
                current_rekvirent_id = known_rekvirent_names[r_rekvirent]
                current_faktura_id = known_fakturaer[current_rekvirent_id]
            else:
                current_rekvirent_id = cls.__find_or_create_rekvirent(rekv_nr=r_rekvirent,
                                                                      shortname=r_shortname,
                                                                      ean_nummer=r_ean_nummer,
                                                                      betalergruppe_id=betalergruppe_id)
                current_faktura_id = cls.__create_faktura(parsing_id=current_parsing.id,
                                                          # pdf_fil      = 'remember to fill this in...',
                                                          rekvirent_id=current_rekvirent_id)

                known_rekvirent_names[r_rekvirent] = current_rekvirent_id
                known_fakturaer[current_rekvirent_id] = current_faktura_id

            # Create the analyse
            Analyse.objects.create(CPR=r_cprnr, afregnings_dato=r_prvdato, svar_dato=r_svardato,
                                   analyse_type_id=analyse_type_id, faktura_id=current_faktura_id)

        # Finish the loop, print info
        t1 = time.perf_counter()
        print('\nDone in %.02f seconds (%.05f sec/row)' %
              ((t1 - t0), ((t1-t0) / total_rows)))

        print("Errors: %d (%.02f%%)" % (len(error_lines), ((len(error_lines)/(total_rows)*100))))
        missing_analyser = [key for key, value in known_analyse_typer.items() if not value]
        print("Unkown analysetypes: %s" % ', '.join(missing_analyser))
        # print(missing_analyser)

        # Write error-files
        print('Writing missing-file to %s' % mangel_liste_file_path)
        cls.subset_of_xlsx(file_path, mangel_liste_file_path, error_lines)

        unknown_analysetyper_file_name = os.path.splitext(os.path.basename(file_path))[
            0] + '_Ukendte_Analyser_' + str(current_parsing.id) + '.xlsx'
        unknown_analysetyper_file_path = os.path.join(
            os.getcwd(), 'backend', 'media', 'mangellister', unknown_analysetyper_file_name)

        print('Writing unknown analysetyper file to %s' % unknown_analysetyper_file_path)
        unk_anal_df = pd.DataFrame(missing_analyser)
        unk_anal_df.columns = ['Ukendte analysetyper']
        unk_anal_df.to_excel(unknown_analysetyper_file_path, index=False)
        
        print('All done')

    def __cleanValues(subject):
        ''' Handles if the input is a float NaN, int or string.\n
        Returns a string or None. '''
        if pd.isnull(subject):
            return None
        elif isinstance(subject, float):
            return str(int(subject))
        elif isinstance(subject, int):
            return str(subject)
        else:
            return subject.strip()

    # @classmethod
    # def __create_parsing(cls, data_fil: str, mangel_liste_fil: str, ptype: str) -> Faktura:
    #     ''' Creates a new parsing and returns it '''
    #     newparse = Parsing.objects.create(
    #         data_fil=data_fil, mangel_liste_fil=mangel_liste_fil, ptype=ptype)
    #     return newparse

    @classmethod
    def __create_faktura(cls, parsing_id: int, rekvirent_id: int) -> int:
        ''' Creates a new faktura and returns its ID '''
        newfakt = Faktura.objects.create(
            parsing_id=parsing_id, rekvirent_id=rekvirent_id)
        return newfakt.id

    @classmethod
    def __find_or_create_rekvirent(cls, rekv_nr: str, shortname: str, ean_nummer: str, betalergruppe_id: int) -> int:
        ''' Looks up the rekvirent, and if none is found, creates one and returns the ID.\n
            Updates the EAN-number as well as the betalergruppe if it is blank but supplied to the function. '''
        try:
            rekvirent = Rekvirent.objects.get(rekv_nr=rekv_nr)
            # Check if GLN-number is null
            if (not rekvirent.GLN_nummer) and ean_nummer:
                rekvirent.GLN_nummer = ean_nummer
                rekvirent.save()
            # Check if betalergruppe is null
            if (not rekvirent.betalergruppe) and betalergruppe_id:
                # rekvirent.betalergruppe = Betalergruppe.objects.get(id=betalergruppe_id)
                rekvirent.betalergruppe_id = betalergruppe_id
                rekvirent.save()

            retval = rekvirent.id
        except ObjectDoesNotExist:
            logger.info("Opretter ny rekvirent: %s (%s)" %
                        (shortname, rekv_nr))
            retval = Rekvirent.objects.create(rekv_nr=rekv_nr,
                                              shortname=shortname,
                                              GLN_nummer=ean_nummer,
                                              betalergruppe_id=betalergruppe_id).id
        return retval

    def __find_or_create_betalergruppe(betalergruppe: str, metatype: str) -> int:
        ''' Looks up the betalergruppe, and if none is found, creates one and returns the ID '''
        try:
            retval = Betalergruppe.objects.get(
                navn=betalergruppe, bgtype=metatype).id
        except ObjectDoesNotExist:
            logger.info("Opretter ny betalergruppe: " + str(betalergruppe))
            retval = Betalergruppe.objects.create(
                navn=betalergruppe, bgtype=metatype).id
        return retval

    def __find_analyse_type_id(labkakode: str):
        ''' Looks up the analyse-code, and returns either the associated ID or None. '''
        try:
            retval = AnalyseType.objects.get(ydelses_kode=labkakode).id
        except ObjectDoesNotExist:
            logger.info(
                "Fejl - Kunne ikke finde analyse med ydelseskode " + labkakode)
            retval = None
        return retval

    def subset_of_xlsx(infile: str, outfile: str, lines_to_include):
        ''' Writes the specified lines in the infile to the outfile. '''
        indf  = pd.read_excel(infile)
        outdf = indf.loc[lines_to_include]
        outdf.to_excel(outfile, index=False)


class Parser:
    @classmethod
    def parse(cls, parsing_object=None, file_path=None):

        print("Parsing...")

        excel_parser = ExcelParser()

        if not file_path:
            file = parsing_object.data_fil
        else:
            file = file_path

        df = pd.read_excel(file, header=None)

        data_source = None

        # Create empty list for the error data
        error_list_list = []

        antal_oprettet = 0
        samlet_pris = 0

        # Denne kunne laves om til en dict
        rekvirent_list = []
        faktura_list = []

        GLN_file = settings.BASE_DIR + '/faktura/assets/patoweb/GLN.xlsx'
        kommune_file = settings.BASE_DIR + '/faktura/assets/patoweb/kommune.xlsx'
        GLN = pd.read_excel(GLN_file)
        kommune = pd.read_excel(kommune_file)

        # Loop through all lines in input xlsx file
        for row in df.iterrows():

            count, method_data = row

            # Parse the data
            # If the data source is blodbank
            if data_source and data_source.lower() == "blodbank":
                # Parse row and save result
                rekvirent = excel_parser.get_blodbank_rekvirent(method_data)
                faktura = None
                analyse = None
                error = ""

                # If the excel_parser returned a rekvirent object
                if not type(rekvirent) is str:
                    # If we have not encountered this rekvirent in this run before
                    if not rekvirent.id in rekvirent_list:
                        # Add the rekvirent ID to rekvirent list and instantiate a faktura object
                        rekvirent_list.append(rekvirent.id)
                        faktura = Faktura.objects.create(
                            parsing=parsing_object, rekvirent=rekvirent)
                        faktura_list.append(faktura)
                    else:
                        # The current faktura is already in the faktura list
                        index = rekvirent_list.index(rekvirent.id)
                        faktura = faktura_list[index]

                    analyse = excel_parser.parse_blodbank(method_data, faktura)

                    if type(analyse) is str:
                        error = analyse
                else:
                    error = rekvirent

                # If there was an error append the data to error list
                if not analyse:
                    method_data["Error"] = error
                    error_list_list.append(method_data)
                elif faktura:
                    faktura.antal_linjer = faktura.antal_linjer + 1
                    faktura.samlet_pris = faktura.samlet_pris + analyse.samlet_pris

            # If the data source is LABKA
            elif data_source and data_source.lower() == "labka":
                # Parse row and save result
                rekvirent = excel_parser.get_labka_rekvirent(method_data)
                faktura = None
                analyse = None
                error = ""

                # If the excel_parser returned a rekvirent object
                if not type(rekvirent) is str:
                    # If we have not encountered this rekvirent in this run before
                    if not rekvirent.id in rekvirent_list:
                        # Add the rekvirent ID to rekvirent list and instantiate a faktura object
                        rekvirent_list.append(rekvirent.id)
                        faktura = Faktura.objects.create(
                            parsing=parsing_object, rekvirent=rekvirent)
                        faktura_list.append(faktura)
                    else:
                        # The current faktura is already in the faktura list
                        index = rekvirent_list.index(rekvirent.id)
                        faktura = faktura_list[index]

                    analyse = excel_parser.parse_labka(method_data, faktura)
                else:
                    error = rekvirent
                # If there was an error append the data to error list
                if not analyse:
                    method_data["Error"] = error
                    error_list_list.append(method_data)
                elif faktura:
                    faktura.antal_linjer = faktura.antal_linjer + 1
                    faktura.samlet_pris = faktura.samlet_pris + analyse.samlet_pris

            elif data_source and data_source.lower() == "patoweb":
                # t0 = time.perf_counter()

                # Parse row and save result
                region = excel_parser.get_patoweb_region(method_data, kommune)
                gln_df = excel_parser.get_patoweb_gln(method_data, GLN)

                if region is None:
                    print("Manglende kommune opslag")
                    print(method_data)
                    error_list_list.append(method_data)
                    continue

                rekvirent = excel_parser.get_patoweb_rekvirent(
                    method_data, gln_df, region)

                faktura = None
                analyse = None

                if rekvirent:
                    tlistrekv_start = time.perf_counter()
                    if not rekvirent.id in rekvirent_list:
                        rekvirent_list.append(rekvirent.id)
                        faktura = Faktura.objects.create(
                            parsing=parsing_object, rekvirent=rekvirent)
                        faktura_list.append(faktura)
                    else:
                        index = rekvirent_list.index(rekvirent.id)
                        faktura = faktura_list[index]

                    analyse = excel_parser.parse_patoweb(
                        method_data, faktura, gln_df, region)

                # If there was an error append the data to error list
                if not analyse:
                    error_list_list.append(method_data)
                elif faktura:
                    faktura.antal_linjer = faktura.antal_linjer + 1
                    faktura.samlet_pris = faktura.samlet_pris + analyse.samlet_pris

                t1 = time.perf_counter()

                # ttotal = t1-t0
                # print("time: " + str(ttotal))

            # During the first row, everything above will have failed, so the data source can be set here
            # Set data source
            if not data_source and str(method_data[0]).lower() == "antal":
                data_source = "blodbank"
                # Set headers for error data
                error_list_list.append(method_data)
            elif not data_source and str(method_data[1]).lower() == "ordinv_id":
                data_source = "labka"
                # Set headers for error data
                error_list_list.append(method_data)
            elif not data_source and str(method_data[0]).lower() == "rekvnr":
                data_source = "patoweb"
                # Set headers for error data
                error_list_list.append(method_data)

            # print(counter)
            sys.stdout.write('\r%d' % count)
            # counter = counter + 1

        print(' lines parsed\nDone parsing lines')
        # Create data frame from error data
        error_list_df = pd.DataFrame(error_list_list)

        # Write to excel-file
        # TODO: Måske find på et bedre filnavn
        mangel_liste_file_name = str(parsing_object.id) + '.xlsx'
        mangel_liste_file_path = os.path.join(
            os.getcwd(), 'backend', 'media', 'mangellister', mangel_liste_file_name)
        with ExcelWriter(mangel_liste_file_path) as writer:
            # writer = ExcelWriter(mangel_liste_file_path)
            error_list_df.to_excel(writer, 'Mangelliste',
                                   index=False, header=None)
            writer.save()
            print('Mangelliste saved at: "%s"' % mangel_liste_file_path)

        parsing_object.mangel_liste_fil = 'mangellister/{}.xlsx'.format(
            parsing_object.id)

        for faktura in faktura_list:
            Faktura.objects.filter(id=faktura.id).update(
                antal_linjer=faktura.antal_linjer)
            Faktura.objects.filter(id=faktura.id).update(
                samlet_pris=faktura.samlet_pris)


class ExcelParser:
    analyse_typer = dict()  # Denne bliver aldrig brugt

    # def create_rekvirent(self, hospital, afdeling, gln_nummer=None):
    #     pass

    def get_or_create_rekvirent(self, hospital, afdeling=None, l4name=None, l6name=None, gln_nummer=None):
        ''' Searches for rekvirent in DB, and if not found, creates it and returns rekvirent object '''
        rekvirent_to_find = None
        if gln_nummer:
            try:  # Implicit antagelse at ingen to rekvirenter har samme GLN
                rekvirent_to_find = Rekvirent.objects.get(
                    GLN_nummer=gln_nummer)
            except ObjectDoesNotExist:
                pass
        elif l4name:
            try:
                rekvirent_to_find = Rekvirent.objects.get(
                    hospital=hospital, niveau='L4Name', afdeling=l4name)
            except ObjectDoesNotExist:
                pass
        elif l6name:
            try:
                rekvirent_to_find = Rekvirent.objects.get(
                    hospital=hospital, niveau='L6Name', afdeling=l6name)
            except ObjectDoesNotExist:
                pass
        else:
            try:
                rekvirent_to_find = Rekvirent.objects.get(
                    hospital=hospital, afdelingsnavn=afdeling)
            except ObjectDoesNotExist:
                rekvirent_to_find = Rekvirent.objects.create(
                    hospital=hospital, afdeling=afdeling)  # TODO: map mulige stier ud

    def get_blodbank_rekvirent(self, method_data):
        ''' Returns either a rekvirent-object or an error string. '''
        YDELSESKODE = method_data[1]
        HOSPITAL = str(method_data[12])
        L4NAME = str(method_data[14])
        L6NAME = str(method_data[17])

        analyse_type = None

        try:
            analyse_type = AnalyseType.objects.get(ydelses_kode=YDELSESKODE)
        except ObjectDoesNotExist:
            logger.info(
                "Fejl - Kunne ikke finde analyse med ydelseskode " + YDELSESKODE)
            return "Fejl - Kunne ikke finde analyse"

        rekvirent = None

        if HOSPITAL == 'Bispebjerg og Frederiksberg Hospitaler':
            try:
                rekvirent = Rekvirent.objects.get(
                    hospital=HOSPITAL, niveau='L6Name', afdelingsnavn=L6NAME)
            except ObjectDoesNotExist:
                try:
                    rekvirent = Rekvirent.objects.get(
                        hospital=HOSPITAL, niveau='L4Name', afdelingsnavn=L4NAME)
                except ObjectDoesNotExist:
                    logger.info("Fejl - Kunne ikke finde rekvirent " +
                                HOSPITAL + " - " + L4NAME + " - " + L6NAME)

        elif HOSPITAL == 'Bornholm':
            if not analyse_type.type == "Analyse":
                logger.info(
                    "Fejl - Bornholm skal kun afregnes for virusanalyser")
                return "Fejl - Bornholm skal kun afregnes for virusanalyser"

            rekvirent = Rekvirent.objects.get(hospital=HOSPITAL)

        elif HOSPITAL == 'Amager og Hvidovre Hospital':
            try:
                rekvirent = Rekvirent.objects.get(
                    hospital=HOSPITAL, niveau='L6Name', afdelingsnavn=L6NAME)
            except ObjectDoesNotExist:
                try:
                    rekvirent = Rekvirent.objects.get(
                        hospital=HOSPITAL, niveau='L4Name', afdelingsnavn=L4NAME)
                except ObjectDoesNotExist:
                    logger.info("Fejl - Kunne ikke finde rekvirent " +
                                HOSPITAL + " - " + L4NAME + " - " + L6NAME)

        elif HOSPITAL == 'Herlev og Gentofte Hospital':
            try:
                rekvirent = Rekvirent.objects.get(
                    hospital=HOSPITAL, niveau='L4Name', afdelingsnavn=L4NAME)
            except ObjectDoesNotExist:
                logger.info("Fejl - Kunne ikke finde rekvirent " +
                            HOSPITAL + " - " + L4NAME + " - " + L6NAME)

            if rekvirent and rekvirent.GLN_nummer == "5798001502092":
                if not analyse_type.type == "Blodprodukt":
                    logger.info(
                        "Fejl - Hud- og allergiafdeling, overafd. U, GE skal kun afregnes for blodprodukter")
                    return "Fejl - Hud- og allergiafdeling, overafd. U, GE skal kun afregnes for blodprodukter"

        # Hvor kommer disse to fra?
        elif HOSPITAL == 'Rigshospitalet' and L4NAME == 'Medicinsk overafd., M GLO':
            rekvirent = Rekvirent.objects.get(GLN_nummer="5798001026031")

        elif HOSPITAL == 'Hospitalerne i Nordsjælland':
            rekvirent = Rekvirent.objects.get(GLN_nummer="5798001068154")

        else:
            logger.info("Fejl - Kunne ikke finde rekvirent " +
                        HOSPITAL + " - " + L4NAME + " - " + L6NAME)

        if rekvirent:
            return rekvirent
        else:
            return "Fejl - Kunne ikke finde rekvirent"

    def parse_blodbank(self, method_data, faktura):
        ''' Returns either an analyse-object or an error string. '''
        ANTAL = method_data[0]
        YDELSESKODE = method_data[1]
        HOSPITAL = method_data[12]
        L4NAME = method_data[14]
        L6NAME = method_data[17]
        # Maybe try/catch here
        SVAR_DATO = datetime.strptime(
            method_data[19], "%Y%m%d").replace(tzinfo=pytz.UTC)
        INSERT_DATO = method_data[20]
        CPR = method_data[21]

        analyse_type = None

        try:
            analyse_type = AnalyseType.objects.get(ydelses_kode=YDELSESKODE)
        except ObjectDoesNotExist:
            logger.info(
                "Fejl - Kunne ikke finde analyse med ydelseskode " + YDELSESKODE)
            return "Fejl - Kunne ikke finde analyse"

        STYK_PRIS = 0

        if analyse_type:

            if math.isnan(ANTAL):
                logger.info(
                    "Fejl - Antallet af analyser ikke angivet for analyse med ydelseskode " + YDELSESKODE)
                return "Fejl - Antallet af analyser ikke angivet"

            for p in analyse_type.priser.order_by('-gyldig_fra'):
                if p.gyldig_fra < now() and (not p.gyldig_til or p.gyldig_til > now()):
                    STYK_PRIS = p.ekstern_pris
                    # Should we have a check for if no price is found?

            SAMLET_PRIS = int(ANTAL) * STYK_PRIS

            analyse = Analyse.objects.create(antal=ANTAL, styk_pris=STYK_PRIS, samlet_pris=SAMLET_PRIS,
                                             CPR=CPR, svar_dato=SVAR_DATO, analyse_type=analyse_type, faktura=faktura)

            return analyse

        return "Ukendt fejl"

    def get_labka_rekvirent(self, method_data):
        ''' Returns either a rekvirent-object or an error string. '''
        YDELSESKODE = method_data[4]
        REKVIRENT = str(method_data[13])
        PAYERCODE = str(method_data[14])
        EAN_NUMMER = str(method_data[21])

        analyse_type = None

        try:
            analyse_type = AnalyseType.objects.get(ydelses_kode=YDELSESKODE)
        except ObjectDoesNotExist:
            logger.info(
                "Fejl - Kunne ikke finde analyse med ydelseskode " + YDELSESKODE)
            return "Fejl - Analyse"

        rekvirent = None

        try:
            rekvirent = Rekvirent.objects.get(
                hospital=REKVIRENT, afdelingsnavn=PAYERCODE, GLN_nummer=EAN_NUMMER)
        except ObjectDoesNotExist:
            rekvirent = Rekvirent.objects.create(
                hospital=REKVIRENT, afdelingsnavn=PAYERCODE, GLN_nummer=EAN_NUMMER)

        return rekvirent

    def parse_labka(self, method_data, faktura):
        ''' Returns either an analyse-object or None. '''
        ANTAL = 1
        CPR = method_data[3]
        YDELSESKODE = method_data[4]
        # Maybe try/catch here
        SVAR_DATO = method_data[10].replace(tzinfo=pytz.UTC)
        REKVIRENT = method_data[13]  # Bruges ikke
        PAYERCODE = method_data[14]  # Bruges ikke
        EAN_NUMMER = method_data[21]

        if not str(EAN_NUMMER):
            logger.info("Fejl - Intet EAN_nummer angivet")
            return None

        analyse_type = None

        try:
            analyse_type = AnalyseType.objects.get(ydelses_kode=YDELSESKODE)
        except ObjectDoesNotExist:
            logger.info(
                "Fejl - Kunne ikke finde analyse med ydelseskode " + YDELSESKODE)

        STYK_PRIS = 0

        if analyse_type:

            if math.isnan(ANTAL):
                logger.info(
                    "Fejl - Antallet af analyser ikke angivet for analyse med ydelseskode " + YDELSESKODE)
                return None

            for p in analyse_type.priser.order_by('-gyldig_fra'):
                if p.gyldig_fra < now() and (not p.gyldig_til or p.gyldig_til > now()):
                    STYK_PRIS = p.ekstern_pris

            SAMLET_PRIS = int(ANTAL) * STYK_PRIS

            analyse = Analyse.objects.create(antal=ANTAL, styk_pris=STYK_PRIS, samlet_pris=SAMLET_PRIS,
                                             CPR=CPR, svar_dato=SVAR_DATO, analyse_type=analyse_type, faktura=faktura)

            return analyse

        return None

    def get_patoweb_rekvirent(self, method_data, gln_df, region):
        ''' Returns either a rekvirent-object or None. '''
        REKVIRENT = str(method_data[0])
        AFD_NAME = str(method_data[7])

        if not gln_df is None:
            # Hvorfor trækkes det først ud her?
            gln_num = gln_df.GLN
        else:
            gln_num = region.lokationsnummer

        rekvirent = None
        gln_num = int(gln_num)

        try:
            rekvirent = Rekvirent.objects.get(
                hospital=REKVIRENT, afdelingsnavn=AFD_NAME, GLN_nummer=gln_num)
        except ObjectDoesNotExist:
            rekvirent = Rekvirent.objects.create(
                hospital=REKVIRENT, afdelingsnavn=AFD_NAME, GLN_nummer=gln_num)

        return rekvirent

    def calculate_patoweb_price(self, method_data, region_navn, hospital):
        points = int(method_data[9])

        for p in PatowebPrisFaktor.objects.all():
            if p.gyldig_fra < now() and (not p.gyldig_til or p.gyldig_til > now()):
                RgH_faktor = p.RgH
                praksis_faktor = p.praksis
                grønland_faktor = p.grønland
                andet_faktor = p.andet

        if region_navn == "Hovedstaden":
            return points * RgH_faktor * 0.5
        elif hospital is None:
            return points * praksis_faktor
        elif region_navn == "Grønland":
            return points * grønland_faktor * 1.1
        else:
            return points * andet_faktor

    def get_patoweb_gln(self, method_data, GLN):
        ''' Returns either an entire row from the GLN-dataframe or None. '''
        rekvafd = method_data[6]

        if not isinstance(rekvafd, str) and not isinstance(rekvafd, int):
            return None

        for j in range(len(GLN)):
            if GLN.rekvafd.iloc[j] == rekvafd:
                return GLN.iloc[j]
                break

        return None

    def get_patoweb_region(self, data, kommune):
        ''' Returns either an entire row from the kommune-dataframe or None. '''
        kommune_kode = data[2]
        if not isinstance(kommune_kode, str):
            return None

        for j in range(len(kommune)):
            if kommune.kommune_nr.iloc[j] == int(kommune_kode):
                return kommune.iloc[j]
                break

        return None

    def parse_patoweb(self, method_data, faktura, gln_row, region):
        region_navn = region.region_navn
        CPR = method_data[1]
        MAT_TYPE = method_data[8]
        SVAR_DATO = method_data[4].replace(tzinfo=pytz.UTC)

        hospital = None
        if not gln_row is None:
            hospital = gln_row.Hospital

        # Denne bruges ikke til noget?
        EAN_NUMMER = int(faktura.rekvirent.GLN_nummer)

        # if not MAT_TYPE in self.analyse_typer.keys(c):
        try:
            analyse_type = AnalyseType.objects.get(ydelses_kode=MAT_TYPE)
        except ObjectDoesNotExist:
            analyse_type = AnalyseType.objects.create(ydelses_kode=MAT_TYPE)

        #     self.analyse_typer[MAT_TYPE] = analyse_type
        # else:
        #     analyse_type = self.analyse_typer[MAT_TYPE]

        pris = self.calculate_patoweb_price(method_data, region_navn, hospital)

        if analyse_type:
            analyse = Analyse.objects.create(antal=1, styk_pris=pris, samlet_pris=pris,
                                             CPR=CPR, svar_dato=SVAR_DATO, analyse_type=analyse_type, faktura=faktura)

            return analyse

        return None
