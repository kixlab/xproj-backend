#!/bin/sh

mv /etc/nginx/sites-available/django_project /etc/nginx/sites-enabled/ && \
nginx -s reload