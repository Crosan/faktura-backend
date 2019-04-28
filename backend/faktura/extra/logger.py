import os

from django.conf import settings
from django.core.files import File

from datetime import datetime


class Logger:

    def log(message):
        current_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    
        file_object = open('./backend/faktura/logs/parserlog.txt', 'a')
        file_object.write(current_time + ' - ' + message + '.\n')
            

        
