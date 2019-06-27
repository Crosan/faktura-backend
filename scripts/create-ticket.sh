#!/bin/bash

CREDENTIALS="/docker/secrets/creds_kt"
. "$CREDENTIALS"
/usr/bin/kinit -kt /docker/secrets/kmad0174.kt kmad0174