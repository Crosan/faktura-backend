from backend.settings.common import *

print("USING TESTING SETTINGS")

DEBUG = False
DEVELOPMENT = False
TESTING = True
PRODUCTION = False

ALLOWED_HOSTS = [
    'localhost',
    'lnxgenmed03.unix.regionh.top.local',
]