from rest_framework import views, status
from rest_framework.response import Response
from django.core import serializers

from backend.faktura.models import *

import json
import pandas as pd
import pytz
from pytz import timezone
from datetime import datetime


class NewPatowebPricesView(views.APIView):    

    def post(self, request, *args, **kwargs):
        print(request.data['file'])
    
        file = request.data['file']
        
        df = pd.read_excel(file)

        priser_dict = {}

        gyldig_fra = None
        gyldig_til = None
        
        for row in df.iterrows():   

            _, data = row

            priser_dict[data[0]] = data[1]

            gyldig_fra, gyldig_til = self.parse_dates(data)


        priser = PatowebPrisFaktor(RgH=priser_dict['RgH'], praksis=priser_dict['praksis'], grønland=priser_dict['grønland'], andet=priser_dict['andet'], gyldig_fra=gyldig_fra, gyldig_til=gyldig_til)

        priser.save()
            
        serialized_prices = serializers.serialize('json', [priser])
        
        return Response(data={"prices": serialized_prices}, status=status.HTTP_200_OK)
    
    def parse_dates(self, data):
        try:
            gyldig_fra = self.to_UTC(data[2])
        except:
            gyldig_fra = now()
            
        try:
            gyldig_til = self.to_UTC(data[3])
        except:
            gyldig_til = None

        return gyldig_fra, gyldig_til

    #Convert datetime
    def to_UTC(self, d : datetime):
        cph_tz = timezone('Europe/Copenhagen')
        return cph_tz.normalize(cph_tz.localize(d)).astimezone(pytz.utc)
        

    #Creates an analyse_pris object
    def create_analyse_pris(self, method_data, analyse_type):
        
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
            
        analyse_pris = AnalysePris(intern_pris=intern_pris, ekstern_pris=ekstern_pris, gyldig_fra=gyldig_fra, gyldig_til=gyldig_til, analyse_type=analyse_type)              
            
        return analyse_pris 
        
        
        
        
        
        
        
        
        
        
        
        
        
        
