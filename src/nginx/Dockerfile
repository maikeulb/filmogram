FROM nginx:1.13.5

RUN rm /etc/nginx/conf.d/default.conf
COPY wait-for-it.sh .
COPY filmogram.conf /etc/nginx/conf.d/

RUN chmod a+x wait-for-it.sh
