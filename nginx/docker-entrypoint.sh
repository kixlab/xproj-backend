#!/bin/sh

cp /etc/nginx/sites-available/django_project /etc/nginx/sites-enabled/

exec nginx -g 'daemon off;'