#!/bin/sh
echo waiting for db
./wait-for-it.sh db:5432 -t 5

flask db upgrade
flask seed-db

echo executing gunicorn
exec gunicorn -b :5000 --access-logfile - --error-logfile - filmogram:app
