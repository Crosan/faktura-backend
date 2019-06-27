#!/bin/bash

SCRIPT="./backend/manage.py"
#CREDENTIALS="/docker/secrets/creds_std"

#. "$CREDENTIALS"

"$SCRIPT" flush --no-input
"$SCRIPT" generate-data
