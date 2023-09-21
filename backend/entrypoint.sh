#!/bin/sh

python manage.py migrate --noinput
python manage.py import_ingredients -p data/ingredients.csv
python manage.py collectstatic --noinput
gunicorn --bind 0.0.0.0:8000 foodgram_backend.wsgi