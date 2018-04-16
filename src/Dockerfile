FROM node:9.6.1 as builder
RUN mkdir /app
WORKDIR /app
COPY package.json /app/package.json
RUN npm install --silent
RUN npm install webpack-cli -g --silent
COPY . /app
RUN npm run build

FROM python:3.6
COPY --from=builder /app /app
COPY . /app
WORKDIR /app

RUN apt-get update && \
    apt-get install -y && \
    pip3 install gunicorn

RUN pip3 install -r /app/requirements.txt
RUN chmod a+x entrypoint.sh
RUN chmod a+x wait-for-it.sh

ENV FLASK_APP=filmogram.py
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

EXPOSE 5000
ENTRYPOINT ["./entrypoint.sh"]
