#!/bin/bash

CREDENTIALS="/docker/secrets/creds_kt"
. "$CREDENTIALS"
/usr/bin/kinit -R