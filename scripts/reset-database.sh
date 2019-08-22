#!/bin/bash

SCRIPT="./manage.py"

"$SCRIPT" flush --no-input
"$SCRIPT" generate-data
