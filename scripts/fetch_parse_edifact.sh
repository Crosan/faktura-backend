#!/bin/bash

SCRIPT="./backend/manage.py"
SECRETS="/docker/secrets"
CREDS_FTP="$SECRETS/creds_ftp"
CREDS_STD="$SECRETS/creds_std"

### SOURCE SETTINGS ###
. "$CREDS_FTP"
. "$CREDS_STD"

"$SCRIPT" "edifact" "OB/EDIFACT" "IB/EDIFACT"
