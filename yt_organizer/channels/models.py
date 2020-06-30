import json
import re
from urllib.parse import urlencode

import dateparser
import requests
import xmltodict
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from parsel import Selector

from channels.managers import VideoQuerySet


class Channel(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    feed_url = models.URLField()

    class Meta:
        verbose_name = "channel"
        verbose_name_plural = "channels"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        match = re.search(
            r"user\/(?P<user_id>.*)|channel\/(?P<channel_id>.*)", self.url,
        )
        if match:
            match_dict = match.groupdict()
            user_id = match_dict.get("user_id")
            if user_id is not None:
                params = {"user": user_id}

            channel_id = match_dict.get("channel_id")
            if channel_id is not None:
                params = {"channel_id": channel_id}

        params = urlencode(params)
        self.feed_url = f"{settings.BASE_YOUTUBE_FEED_URL}?{params}"
        super().save(*args, **kwargs)

    def sync_videos(self):
        response = requests.get(self.feed_url)
        channel_feed = xmltodict.parse(response.text)

        existing_videos = list(self.videos.values_list("video_id", flat=True))
        latest_videos = channel_feed["feed"]["entry"]
        for entry in latest_videos:
            video_id = entry["yt:videoId"]
            if video_id not in existing_videos:
                video = Video.objects.create(
                    url=entry["link"]["@href"],
                    title=entry["title"],
                    channel=self,
                    thumbnail_image=entry["media:group"]["media:thumbnail"]["@url"],
                    published_date=dateparser.parse(entry["published"]),
                )
                Feed.objects.create(video=video, feed=json.dumps(entry))


class Video(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=255)
    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
        related_name="videos",
        related_query_name="video",
    )
    video_id = models.CharField(max_length=20, unique=True)
    thumbnail_image = models.URLField()
    published_date = models.DateTimeField()

    objects = VideoQuerySet.as_manager()

    class Meta:
        verbose_name = "video"
        verbose_name_plural = "videos"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.video_id:
            match = re.search(r"\?v=(?P<video_id>.*)", self.url)
            if match:
                match_dict = match.groupdict()
                video_id = match_dict.get("video_id", "")
                self.video_id = video_id
        super().save(*args, **kwargs)


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    public = models.BooleanField(default=False)
    channels = models.ManyToManyField(
        Channel, related_name="category", related_query_name="categories"
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Feed(models.Model):
    video = models.OneToOneField(Video, on_delete=models.CASCADE)
    feed = models.TextField()
