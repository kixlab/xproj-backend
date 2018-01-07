#!/bin/sh

certbot -n certonly --standalone --force-renewal --preferred-challenges http -d api.budgetwiser.org --agree-tos --email grau@kaist.ac.kr