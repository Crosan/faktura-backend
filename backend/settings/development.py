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