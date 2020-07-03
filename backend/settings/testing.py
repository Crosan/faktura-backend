from backend.settings.common import *

print("USING TESTING SETTINGS")

DEBUG = False
DEVELOPMENT = False
TESTING = True
PRODUCTION = False

ALLOWED_HOSTS = [
    'localhost',
    'tlnxautodiaf02.unix.regionh.top.local',
]

DATABASES = {
    'default': {
        'NAME': os.environ.get('DJANGO_DB_NAME'),
        'ENGINE': os.environ.get('DJANGO_DB_ENGINE'),
        'HOST': os.environ.get('DJANGO_DB_HOST'),
        'PORT': os.environ.get('DJANGO_DB_PORT'),
        'USER': os.environ.get('DJANGO_DB_USER'),
        'PASSWORD': os.environ.get('DJANGO_DB_PASSWORD'),
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'extra_params': 'trusted_connection=yes'
        },
    }
}
