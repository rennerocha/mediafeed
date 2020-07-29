#!/bin/sh

printenv | grep -v "no_proxy" >> /etc/environment

python manage.py crontab add
python manage.py collectstatic --noinput
python manage.py migrate
cron

gunicorn --workers=2 --bind=0.0.0.0:8000 mediafeed.wsgi:application
