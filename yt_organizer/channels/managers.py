import datetime

from django.db import models
from django.utils import timezone


class VideoQuerySet(models.QuerySet):
    def last_24h(self):
        from channels.models import Video

        start_datetime = timezone.now().replace(microsecond=0) - datetime.timedelta(
            hours=24
        )
        return Video.objects.filter(published_date__gte=start_datetime)

    def last_week(self):
        from channels.models import Video

        start_datetime = timezone.now().replace(microsecond=0) - datetime.timedelta(
            days=7
        )
        return Video.objects.filter(published_date__gte=start_datetime)

    def for_categories(self, categories):
        from channels.models import Video

        return Video.objects.filter(channel__categories__in=categories)
