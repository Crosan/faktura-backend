import os

from rest_framework import serializers
from backend.faktura.models import *
from backend.faktura.exceptions import *

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
        
class ParsingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParsingStatus
        fields = "__all__"
        
class ReceiptFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiptFile
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
    rekvirent = RekvirentSerializer()

    class Meta:
        model = Analyse
        fields = "__all__"
        
        
class NestedRekvirentSerializer(serializers.ModelSerializer):
    analyser = AnalyseSerializer(many=True)

    class Meta:
        model = Rekvirent
        fields = "__all__"
        
class NestedParsingSerializer(serializers.ModelSerializer):
    analyser = AnalyseSerializer(many=True)
    oprettet_af = ProfileSerializer()
    status_historik = ParsingStatusSerializer(many=True)

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
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        