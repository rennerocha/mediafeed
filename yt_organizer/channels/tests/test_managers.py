import datetime

from django.test import TestCase
from model_bakery import baker

from channels.models import Category, Channel, Video


class VideoManagerTestCase(TestCase):
    def setUp(self):
        self.channel = baker.make(Channel)

    def test_last_24h(self):
        last_24h = datetime.datetime.now() - datetime.timedelta(hours=24)
        older_than_24h = last_24h + datetime.timedelta(seconds=1)

        video_last_24h = baker.make(Video, published_date=last_24h)
        older_video = baker.make(Video, published_date=older_than_24h)

        videos = Video.objects.last_24h()

        self.assertTrue(video_last_24h in videos)
        self.assertTrue(older_video not in videos)

    def test_last_week(self):
        last_week = datetime.datetime.now() - datetime.timedelta(days=7)
        older_than_week = last_week + datetime.timedelta(seconds=1)

        video_last_week = baker.make(Video, published_date=last_week)
        older_than_week_video = baker.make(Video, published_date=older_than_week)

        videos = Video.objects.last_week()

        self.assertTrue(video_last_week in videos)
        self.assertTrue(older_than_week_video not in videos)

    def test_videos_for_categories(self):
        category_1 = baker.make(Category)
        channel_1 = baker.make(Channel)
        video_1 = baker.make(Video, channel=channel_1)
        category_1.channels.add(channel_1)

        category_2 = baker.make(Category)
        channel_2 = baker.make(Channel)
        video_2 = baker.make(Video, channel=channel_2)
        category_2.channels.add(channel_2)

        category_3 = baker.make(Category)
        channel_3 = baker.make(Channel)
        video_3 = baker.make(Video, channel=channel_3)
        category_3.channels.add(channel_3)

        categories = Category.objects.filter(
            title__in=[category_1.title, category_2.title]
        )
        videos = Video.objects.for_categories(categories)

        self.assertTrue(video_1 in videos)
        self.assertTrue(video_2 in videos)
        self.assertTrue(video_3 not in videos)

    def test_videos_last_24h_videos_for_categories(self):
        category_1 = baker.make(Category)
        channel_1 = baker.make(Channel)

        last_24h = datetime.datetime.now() - datetime.timedelta(hours=24)
        older_than_24h = last_24h + datetime.timedelta(seconds=1)

        video_1 = baker.make(Video, channel=channel_1, published_date=last_24h)
        video_2 = baker.make(Video, channel=channel_1, published_date=last_24h)
        video_3 = baker.make(Video, channel=channel_1, published_date=older_than_24h)
        video_4 = baker.make(Video, channel=channel_1, published_date=older_than_24h)

        categories = Category.objects.filter(title__in=[category_1.title])
        videos = Video.objects.for_categories(categories).last_24h()

        self.assertTrue(video_1 in videos)
        self.assertTrue(video_2 in videos)
        self.assertTrue(video_3 not in videos)
        self.assertTrue(video_4 not in videos)

    def test_videos_last_week_videos_for_categories(self):
        category_1 = baker.make(Category)
        channel_1 = baker.make(Channel)

        last_week = datetime.datetime.now() - datetime.timedelta(days=7)
        older_than_week = last_week + datetime.timedelta(seconds=1)

        video_1 = baker.make(Video, channel=channel_1, published_date=last_week)
        video_2 = baker.make(Video, channel=channel_1, published_date=last_week)
        video_3 = baker.make(Video, channel=channel_1, published_date=older_than_week)
        video_4 = baker.make(Video, channel=channel_1, published_date=older_than_week)

        categories = Category.objects.filter(title__in=[category_1.title])
        videos = Video.objects.for_categories(categories).last_week()

        self.assertTrue(video_1 in videos)
        self.assertTrue(video_2 in videos)
        self.assertTrue(video_3 not in videos)
        self.assertTrue(video_4 not in videos)
