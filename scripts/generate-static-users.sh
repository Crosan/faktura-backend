#!/bin/bash

SCRIPT="./manage.py"
STD_CREDENTIALS="/docker/secrets/creds_std"
MS_CREDENTIALS="/docker/secrets/creds_ms"
KT_CREDENTIALS="/docker/secrets/creds_kt"

. "$STD_CREDENTIALS"
. "$MS_CREDENTIALS"
. "$KT_CREDENTIALS"

"$SCRIPT" generate-static-users
