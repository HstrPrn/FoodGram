#!/bin/sh

python manage.py makemigrations
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py import_ingredients -f ingredients.csv
python manage.py import_tags -f tags.csv
DJANGO_SUPERUSER_PASSWORD=${SUPERUSER_PASSWORD} python manage.py \
    createsuperuser --noinput --email ${SUPERUSER_EMAIL} --username \
    ${SUPERUSER_USERNAME} --first_name ${SUPERUSER_FIRST_NAME} --last_name \
    ${SUPERUSER_LAST_NAME}
gunicorn --bind 0.0.0.0:8000 foodgram_backend.wsgi