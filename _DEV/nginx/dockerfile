FROM alpine:3.4

RUN apk add --update nginx && rm -rf /var/cache/apk/*

ADD nginx.conf /etc/nginx/nginx.conf

RUN mkdir /www-data

EXPOSE 80

CMD ["nginx"]