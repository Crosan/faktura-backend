from backend.settings.common import *

DEBUG = True
DEVELOPMENT = True
TESTING = False
PRODUCTION = False

ALLOWED_HOSTS = [
    'localhost',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'sql_server.pyodbc',
#         'NAME': 'AutoDIA_faktura_01',
#         'USER': '***REMOVED***@RGHSQLHOTEL003B',
#         'PASSWORD': '***REMOVED***',
#         'HOST': 'RGHSQLHOTEL003B',
#         'PORT': '1433',

#         'OPTIONS': {
#             'driver': 'ODBC Driver 13 for SQL Server',
#         },
#     },
# }
