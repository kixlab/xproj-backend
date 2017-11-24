#!/bin/sh

certbot -n certonly --webroot -w /var/www/api.budgetwiser.org/ -d api.budgetwiser.org --agree-tos --email grau@kaist.ac.kr && \
mv /etc/nginx/sites-available/django_project /etc/nginx/sites-enabled/ && \
nginx -s reload