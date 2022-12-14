#!/bin/bash

CONTAINER_FIRST_STARTUP="CONTAINER_FIRST_STARTUP"
if [ ! -e /$CONTAINER_FIRST_STARTUP ]; then
    touch /$CONTAINER_FIRST_STARTUP
    echo "waiting for DB ready for 10 seconds"
    sleep 10
    echo "Preparing Migrations migrations"
    python3 manage.py makemigrations
    echo "Runing migrations"
    python3 manage.py migrate
    echo "Loading Test data, the procedure may take a couple minutes"
    python3 manage.py load_prefixes fixtures/routes.txt
    echo "Staring Gunicorn"
    gunicorn prefix_resolver.wsgi:application --bind 0:8000
else
    echo "ReStaring Gunicorn"
    gunicorn prefix_resolver.wsgi:application --bind 0:8000
fi
