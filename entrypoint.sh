#!/usr/bin/env sh
set -e
python manage.py migrate --noinput || true
python manage.py collectstatic --noinput || true
exec gunicorn wiremit_backend.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120
