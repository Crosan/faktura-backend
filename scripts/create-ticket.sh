#!/bin/bash

CREDENTIALS="/docker/secrets/creds_kt"
. "$CREDENTIALS"
/usr/bin/kinit -kt /docker/secrets/kerberos.kt "$KEYTAB_PRINCIPAL"
