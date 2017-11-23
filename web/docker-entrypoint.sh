#!/bin/sh

python3 manage.py collectstatic --noinput

exec /usr/bin/gunicorn config.wsgi:application -w 2 -b :8000 --timeout 30 --log-level=DEBUG
