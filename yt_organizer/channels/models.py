from django.db import models


class Channel(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    channel_id = models.CharField(max_length=100)


class Video(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=255)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    video_id = models.CharField(max_length=100)
    thumbnail_image = models.URLField()
    published_date = models.DateField()


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    channels = models.ManyToManyField(Channel)


class Feed(models.Model):
    video = models.OneToOneField(Video, on_delete=models.CASCADE)
    feed = models.TextField()
