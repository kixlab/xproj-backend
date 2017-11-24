FROM nginx:1.13.7-alpine

RUN apk add --no-cache certbot

RUN mkdir -p /var/www/api.budgetwiser.org/

ADD nginx.conf /etc/nginx/conf.d/nginx.conf
ADD sites-enabled/ /etc/nginx/sites-enabled
ADD sites-available/ /etc/nginx/sites-available

ADD ./init_letsencrypt.sh /init_letsencrypt.sh
RUN chmod +x /init_letsencrypt.sh

RUN ln -sf /dev/stdout /var/log/nginx/access.log
RUN ln -sf /dev/stderr /var/log/nginx/error.log

# RUN echo '0  7  1,15  *  *    certbot renew --pre-hook "service nginx stop" --post-hook "service nginx start"' > /etc/crontabs/root
