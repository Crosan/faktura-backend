import os

from rest_framework import serializers
from backend.backend.models import *


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
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        