#!/bin/sh

nginx && \
certbot -n certonly --webroot -w /var/www/acme-challenge/ -d api.budgetwiser.org --agree-tos --email grau@kaist.ac.kr