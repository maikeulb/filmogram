FROM python:3.6

COPY . /app
WORKDIR /app

RUN apt-get update && \
    apt-get install -y && \
    pip3 install gunicorn

RUN pip3 install -r /app/requirements.txt
RUN chmod a+x entrypoint.sh
RUN chmod a+x wait-for-it.sh

ENV FLASK_APP=filmogram.py
ENV FLASK_APP_CONFIG=config.ProductionConfig
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

EXPOSE 5000
ENTRYPOINT ["./entrypoint.sh"]
