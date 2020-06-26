import datetime

from django.db import models


class VideoManager(models.Manager):
    def last_24h(self):
        from channels.models import Video

        start_datetime = datetime.datetime.utcnow() - datetime.timedelta(hours=24)
        return Video.objects.filter(published_date__lte=start_datetime)

    def last_week(self):
        from channels.models import Video

        start_datetime = datetime.datetime.utcnow() - datetime.timedelta(days=7)
        return Video.objects.filter(published_date__lte=start_datetime)
