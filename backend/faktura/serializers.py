import os

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
    class Meta:
        model = AnalyseType
        fields = "__all__"
        
class RekvirentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rekvirent
        fields = "__all__"
        
class ParsingSerializer(serializers.ModelSerializer):
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
    
        
class FakturaSerializer(serializers.ModelSerializer):
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
        
class FakturaStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = FakturaStatus
        fields = "__all__"
               
class BetalergruppeSerializer(serializers.ModelSerializer):
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
        
        Parser.parse(parsing_obj)
        
        return parsing_obj
        
class NestedBetalergruppeSerializer(serializers.ModelSerializer):
    rekvirenter = NestedRekvirentSerializer(many=True, required=False)

    class Meta:
        model = Betalergruppe
        fields = "__all__"

# ------------------------
# ONE LEVEL NESTED SERIALIZERS
# ------------------------       

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
        









