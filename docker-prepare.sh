#!/usr/bin/env bash

set -ex
echo "PWD=$PWD"

python manage.py collectstatic --noinput
