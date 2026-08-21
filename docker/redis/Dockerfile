FROM redis:8-alpine

COPY redis.conf /usr/local/etc/redis/redis.conf
COPY sentinel.conf /usr/local/etc/redis/sentinel.conf

RUN chown -R redis:redis /usr/local/etc/redis \
    && chmod 755 /usr/local/etc/redis \
    && chmod 664 /usr/local/etc/redis/sentinel.conf

EXPOSE 6379 26379