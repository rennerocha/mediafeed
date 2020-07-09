import datetime

from django.db import models
from django.utils import timezone


class VideoQuerySet(models.QuerySet):
    def last_24h(self):
        start_datetime = timezone.now() - datetime.timedelta(hours=24, minutes=1)
        return self.filter(published_date__gte=start_datetime)

    def last_week(self):
        start_datetime = timezone.now() - datetime.timedelta(days=7, minutes=1)
        return self.filter(published_date__gte=start_datetime)

    def for_categories(self, categories):
        return self.filter(channel__categories__in=categories)
