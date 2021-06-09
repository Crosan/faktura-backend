import logging
import os
import threading
import traceback

from rest_framework import serializers
from backend.faktura.models import *
from backend.faktura.exceptions import *
from backend.faktura.extra.parser import Parser

import ntpath

def getFileType(file):
    _, file_extension = os.path.splitext(file.name)
    return file_extension


# ------------------------
# REGULAR SERIALIZERS
# ------------------------

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        
class AnalyseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analyse
        fields = "__all__"
        
class AnalysePrisSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysePris
        fields = "__all__"        
        
class AnalyseTypeSerializer(serializers.ModelSerializer):
    antal = serializers.IntegerField(read_only=True)
    pris = serializers.FloatField(read_only=True)

    class Meta:
        model = AnalyseType
        fields = "__all__"
        
class RekvirentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rekvirent
        fields = "__all__"
        
class ParsingSerializer(serializers.ModelSerializer):
    antal_fakturaer = serializers.IntegerField(read_only=True)
    samlet_pris = serializers.FloatField(read_only=True)

    class Meta:
        model = Parsing
        fields = "__all__"
        
    def validate(self, data):
        """ Check the filetype of the 'parsing' file is allowed types """
        file_ext = getFileType(data['data_fil'])
        if file_ext != '.xlsx':
            raise ParsingFileTypeValidation(
                'Parsing filetype must be .xlsx', 'data_fil', status_code=status.HTTP_400_BAD_REQUEST)

        return data       
    
class DebitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Debitor
        fields = "__all__"
        
class FakturaSerializer(serializers.ModelSerializer):
    antal_analyser = serializers.IntegerField(
        read_only=True
    )

    samlet_pris = serializers.FloatField(read_only=True)

    class Meta:
        model = Faktura
        fields = "__all__"
        
    # def validate(self, data):
    #     """ Check the filetype of the 'faktura' file is allowed types   
    #     Overridden to always be true by RS 2021/05/14 """
    #     return True
    #     file_ext = getFileType(data['pdf_fil'])
    #     if file_ext != '.pdf':
    #         raise ParsingFileTypeValidation(
    #             'Faktura filetype must be .pdf', 'pdf_fil', status_code=status.HTTP_400_BAD_REQUEST)

    #     return data
        
class FakturaStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = FakturaStatus
        fields = "__all__"
               
class BetalergruppeSerializer(serializers.ModelSerializer):
    sum_total = serializers.FloatField(read_only=True)
    sum_unsent = serializers.FloatField(read_only=True)
    antal = serializers.IntegerField(read_only=True)
    antal_unsent = serializers.IntegerField(read_only=True)
    class Meta:
        model = Betalergruppe
        fields = "__all__"
        
# ------------------------
# NESTED SERIALIZERS
# ------------------------

class NestedAnalyseTypeSerializer(serializers.ModelSerializer):
    priser = AnalysePrisSerializer(many=True)

    class Meta:
        model = AnalyseType
        fields = "__all__"
        

class NestedAnalyseSerializer(serializers.ModelSerializer):
    analyse_type = NestedAnalyseTypeSerializer()

    class Meta:
        model = Analyse
        fields = "__all__"
        
        
class NestedRekvirentSerializer(serializers.ModelSerializer):
    # fakturaer = FakturaSerializer(many=True)
    betalergruppe = BetalergruppeSerializer()

    class Meta:
        model = Rekvirent
        fields = "__all__"
        
class NestedFakturaSerializer(serializers.ModelSerializer):
    # analyser = NestedAnalyseSerializer(many=True) #Udkommenteret af RS, 31/03/21
    antal_analyser = serializers.IntegerField(
        read_only=True
    )
    samlet_pris = serializers.FloatField(read_only=True)
    cpr = serializers.IntegerField(read_only=True)

    rekvirent = NestedRekvirentSerializer()

    class Meta:
        model = Faktura
        fields = "__all__"
        
    def validate(self, data):
        """ Check the filetype of the 'faktura' file is allowed types """
        file_ext = getFileType(data['pdf_fil'])
        if file_ext != '.pdf':
            raise ParsingFileTypeValidation(
                'Faktura filetype must be .pdf', 'pdf_fil', status_code=status.HTTP_400_BAD_REQUEST)

        return data
        
        
class NestedParsingSerializer(serializers.ModelSerializer):
    #oprettet_af = ProfileSerializer()
    fakturaer = NestedFakturaSerializer(many=True, required=False)

    class Meta:
        model = Parsing
        fields = "__all__"
        
    def validate(self, data):
        """ Check the filetype of the 'parsing' file is allowed types """
        file_ext = getFileType(data['data_fil'])
        if file_ext != '.xlsx':
            raise ParsingFileTypeValidation(
                'Parsing filetype must be .xlsx', 'data_fil', status_code=status.HTTP_400_BAD_REQUEST)

        return data
        
    def create(self, validated_data):
        try:
            test = validated_data.get('fakturaer')
            
            if test is not None:
                validated_data.pop('fakturaer')
        except:
            print("No faktura list sent")
    
        parsing_obj = Parsing.objects.create(**validated_data)
        
        t = threading.Thread(target=self.parseWrap, args=[parsing_obj])
        t.start()
        # return True
        # Parser.parse(parsing_obj)
        
        return parsing_obj

    def parseWrap(self, parsing_object):
        logger = logging.getLogger("app")
        print('wrapper called with path: %s' % parsing_object)
        parser = Parser()
        try:
            parser.parse(parsing_object)
        except Exception as e:
            print(e)
            parsing_object.status = 'Fejlet: ' + traceback.format_exc()
            logger.error('Parsing failed')
            logger.info(traceback.format_exc())
            parsing_object.save()
        # except:
        #     parsing_object.status = 'Fejlet: Ukendt fejl'
        #     parsing_object.save()
        
class NestedBetalergruppeSerializer(serializers.ModelSerializer):
    rekvirenter = NestedRekvirentSerializer(many=True, required=False)

    class Meta:
        model = Betalergruppe
        fields = "__all__"

# ----------------------------
# ONE LEVEL NESTED SERIALIZERS
# ----------------------------       

class SemiNestedParsingSerializer(serializers.ModelSerializer):
    '''
    Returns parsing, nested only one level (i.e. fakturaer in parse is included, but analyser in fakturaer are not)
    '''
    fakturaer = FakturaSerializer(many=True, required=False)

    class Meta:
        model = Parsing
        fields = "__all__"
        

class SemiNestedFakturaSerializer(serializers.ModelSerializer):
    '''
    Returns faktura, nested only one level (i.e. analyser in faktura is included, but analysetypes in analyser are not)
    '''
    analyser = AnalyseSerializer(many=True, required=False)

    class Meta:
        model = Faktura
        fields = "__all__"
        


# ------------------------
# SPECIAL VIEW SERIALIZERS
# ------------------------

class PPBetalergruppeSerializer(serializers.ModelSerializer):
    # rekvirenter = RekvirentWithFaktSerializer(many=True, required=False)
    sum_total = serializers.FloatField()

    class Meta:
        model = Betalergruppe
        fields = ('id', 'navn', 'sum_total')

class RekvirentWithFaktSerializer(serializers.ModelSerializer):
    fakturaer = FakturaSerializer(many=True)

    class Meta:
        model = Rekvirent
        fields = "__all__"
