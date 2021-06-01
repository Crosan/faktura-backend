import os
import ldap
from django_auth_ldap.config import GroupOfNamesType, LDAPSearchUnion, LDAPSearch
from backend.settings.common import *
import pyodbc


print("USING TESTING SETTINGS")

DEBUG = False
DEVELOPMENT = False
TESTING = True
PRODUCTION = False

SECRET_KEY = os.environ.get('DJANGO_SECRET')

ALLOWED_HOSTS = [
    'localhost',
    'lnxgenmed02.unix.regionh.top.local',
    'tlnxautodiaf02.unix.regionh.top.local',
    'tlnxautodiaf03.unix.regionh.top.local' 
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [       
        'backend.faktura.app.authentication.FakturaAuthentication', # custom authentication class
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

###########
#  LDAP   #
###########

# Binding and connection options
AUTH_LDAP_SERVER_URI = os.environ.get('LDAP_HOST')
AUTH_LDAP_BIND_DN = os.environ.get('LDAP_BIND_DN')
AUTH_LDAP_BIND_PASSWORD = os.environ.get('LDAP_BIND_PASSWORD')

AUTH_LDAP_GLOBAL_OPTIONS = {
    ldap.OPT_DEBUG_LEVEL: 0,
    ldap.OPT_REFERRALS: 0,
    ldap.OPT_X_TLS_REQUIRE_CERT: ldap.OPT_X_TLS_NEVER,
}
AUTH_LDAP_USER_SEARCH = LDAPSearchUnion(
    LDAPSearch("""OU=Users,OU=RH,OU=Region Hovedstaden, DC=regionh,DC=top,DC=local""", ldap.SCOPE_SUBTREE, "(BamUserId=%(user)s)"),
    LDAPSearch("""OU=Service brugere,OU=RegionH Administration,DC=regionh,DC=top,DC=local""", ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)")
)

# Search for groups
AUTH_LDAP_GROUP_SEARCH = LDAPSearch("""OU=GeM,OU=Ressource Grupper,
                                       OU=FAELLES Administration,
                                       OU=Region Hovedstaden,
                                       DC=regionh,DC=top,DC=local""", 
                                       ldap.SCOPE_SUBTREE, "(objectClass=group)")

AUTH_LDAP_GROUP_TYPE = GroupOfNamesType()

AUTH_LDAP_USER_ATTR_MAP = {
    "display_name": "displayName",
    "telephone": "telephoneNumber",
    "email": "mail",
    "title": "title"
}

AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    'er_akademiker':        'CN=RGH-B-SE GEM AC,OU=GeM,OU=Ressource Grupper, OU=FAELLES Administration, OU=Region Hovedstaden, DC=regionh,DC=top,DC=local',
    'er_admin':             'CN=RGH-B-SE GEM Admin,OU=GeM,OU=Ressource Grupper, OU=FAELLES Administration, OU=Region Hovedstaden, DC=regionh,DC=top,DC=local',
    'er_bioanalytiker':     'CN=RGH-B-SE GEM Bioanalytiker,OU=GeM,OU=Ressource Grupper, OU=FAELLES Administration, OU=Region Hovedstaden, DC=regionh,DC=top,DC=local',
    'er_bioinformatiker':   'CN=RGH-B-SE GEM Bioinformatiker,OU=GeM,OU=Ressource Grupper, OU=FAELLES Administration, OU=Region Hovedstaden, DC=regionh,DC=top,DC=local',
    'er_sekretaer':         'CN=RGH-B-SE GEM Sekretaer,OU=GeM,OU=Ressource Grupper, OU=FAELLES Administration, OU=Region Hovedstaden, DC=regionh,DC=top,DC=local',
    'er_studerende':        'CN=RGH-B-SE GEM Studerende,OU=GeM,OU=Ressource Grupper, OU=FAELLES Administration, OU=Region Hovedstaden, DC=regionh,DC=top,DC=local'
}

# This is the default, but I like to be explicit.
AUTH_LDAP_ALWAYS_UPDATE_USER = True

# Use LDAP group membership to calculate group permissions.
AUTH_LDAP_FIND_GROUP_PERMS = True

AUTHENTICATION_BACKENDS = [
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
]

############
# Database #
############

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

drivers = [item for item in pyodbc.drivers()]
driver = drivers[-1]
print("driver:{}".format(driver))

DATABASES = {
    'default': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': 'AutoDIA_faktura_01',
        'USER': 'AutoDIAfaktura_user@localhost',
        'PASSWORD': 'Ho##265sKilg!!',
        'HOST': 'RGHSQLHOTEL003B,1433',
        # 'PORT': '1433',

        'OPTIONS': {
            # 'driver': 'ODBC Driver 13 for SQL Server',
            'driver': 'ODBC Driver 17 for SQL Server',
            # 'driver': driver,
        },
    },
}

# set this to False if you want to turn off pyodbc's connection pooling
# DATABASE_CONNECTION_POOLING = False

###########
# Logging #
###########

LOG_DIR = os.environ.get('LOG_DIR')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'django.log'),
            'maxBytes': 1024*1024*5,  # 5MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s|%(asctime)s|%(module)s|%(process)d|%(thread)d|%(message)s',
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s|%(message)s'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'logfile'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'logfile'],
            'level': 'INFO',
            'propagate': False,
        },
        'django_auth_ldap': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}