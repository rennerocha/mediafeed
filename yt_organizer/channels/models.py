import re
from urllib.parse import urlencode

import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from parsel import Selector


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


class Video(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=255)
    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
        related_name="videos",
        related_query_name="video",
    )
    video_id = models.CharField(max_length=100)
    thumbnail_image = models.URLField()
    published_date = models.DateField()

    class Meta:
        verbose_name = "video"
        verbose_name_plural = "videos"

    def __str__(self):
        return self.title


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
