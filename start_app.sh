#!/bin/sh

printenv | grep -v "no_proxy" >> /etc/environment

echo "*/30 * * * * PATH=/usr/local/bin /sync_channels.sh >> /var/log/cron.log 2>&1
# This extra line makes it a valid cron" > scheduler.txt
crontab scheduler.txt
cron

python manage.py collectstatic --noinput
python manage.py migrate
gunicorn --workers=2 --bind=0.0.0.0:8000 yt_organizer.wsgi:application
