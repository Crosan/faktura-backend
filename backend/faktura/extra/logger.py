import os

from django.conf import settings
from django.core.files import File


class Logger:

    def log(message):
        file_object = open('./backend/faktura/logs/parserlog.txt', 'a')
        file_object.write(message + '.\n')
            

        
