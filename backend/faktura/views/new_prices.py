from rest_framework import views, status
from rest_framework.response import Response
from django.core import serializers

from backend.faktura.models import *

import json
import pandas as pd
import pytz
import math
from pytz import timezone
from datetime import datetime


class NewPricesView(views.APIView):    

    def post(self, request, *args, **kwargs):
        
        #Convert datetime
        def to_UTC(self, d : datetime):
            cph_tz = timezone('Europe/Copenhagen')
            return cph_tz.normalize(cph_tz.localize(d)).astimezone(pytz.utc)
            
        #Gets the relevant analyse_type object
        def get_analyse_type(method_data):
        
            ydelses_kode = method_data[0]
            ydelses_navn = method_data[1]
            # gruppering = method_data[2]
            # kilde_navn = method_data[3]
            # afdeling = method_data[6]
            
            # if not isinstance(gruppering, str):
            #     gruppering = ""
                
            # if not isinstance(kilde_navn, str):
            #     kilde_navn = ""
            
            # type = ""
            
            # if afdeling == "KI":
            #     if ydelses_kode.startswith('T') or ydelses_kode.endswith('A'):
            #         type = "Analyse"
            #     else:
            #         type = "Blodprodukt"
                    
            try:
                analyse_type = AnalyseType.objects.get(ydelses_kode=method_data[0])   
            except:
                analyse_type = AnalyseType(ydelses_kode=ydelses_kode, ydelses_navn=ydelses_navn)
            
            return analyse_type
    
        #Creates an analyse_pris object
        def create_analyse_pris(method_data, analyse_type):
            # print(type(method_data[7]), method_data[7])

            # intern_pris = method_data[4]
            ekstern_pris = method_data[3]
            # try:
            #     gyldig_fra = to_UTC(method_data[7])
            # except:
            #     gyldig_fra = now()
                
            # try:
            #     gyldig_til = to_UTC(method_data[8])
            # except:
            #     gyldig_til = None
                
            if isinstance(method_data[4], datetime):
                gyldig_fra = method_data[4]
            else:
                gyldig_fra = now()

            if isinstance(method_data[5], datetime):
                gyldig_til = method_data[5]
            else:
                gyldig_til = None

            analyse_pris = AnalysePris(ekstern_pris=ekstern_pris, gyldig_fra=gyldig_fra, gyldig_til=gyldig_til, analyse_type=analyse_type)              
                
            return analyse_pris 
            
        print(request.data['file'])
    
        file = request.data['file']
        
        df = pd.read_excel(file, header=None, na_filter=False)
        
        data_found = False
        
        new_prices = []
        analyse_type_objects = []

        new_analyse_typer = []
        
        for row in df.iterrows():   

            _, method_data = row
            
            if not data_found:
                if str(method_data[0]).lower() == "ydelseskode":
                    data_found = True
                    continue            
                continue 
                
            analyse_type = get_analyse_type(method_data)
            
            if not analyse_type.id:
                new_analyse_typer.append(analyse_type)
            
            if analyse_type.id: 
                analyse_pris = create_analyse_pris(method_data, analyse_type)
            
                new_prices.append(analyse_pris)
                analyse_type_objects.append(AnalyseType.objects.get(pk=analyse_pris.analyse_type.id))
            
        serialized_prices = serializers.serialize('json', new_prices)
        serialized_types = serializers.serialize('json', new_analyse_typer)
        serialized_analyse_type_objects = serializers.serialize('json', analyse_type_objects)
        
        return Response(data={"prices": serialized_prices, "new_analyse_typer": serialized_types, "analyse_type_objects": serialized_analyse_type_objects}, status=status.HTTP_200_OK)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
