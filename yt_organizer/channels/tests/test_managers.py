import datetime

from django.test import TestCase
from django.utils import timezone
from model_bakery import baker

from channels.models import Category, Channel, Video


class VideoManagerTestCase(TestCase):
    def setUp(self):
        self.channel = baker.make(Channel)

    def test_last_24h_videos(self):
        just_now = timezone.now()
        last_24h = just_now - datetime.timedelta(hours=24)
        older_than_24h = last_24h - datetime.timedelta(minutes=1)

        video_just_now = baker.make(
            Video, title="Video Just Now", published_date=just_now
        )
        video_last_24h = baker.make(
            Video, title="Video 24h Ago", published_date=last_24h
        )
        video_older_than_24h = baker.make(
            Video, title="Video 24h Ago + 1 minute", published_date=older_than_24h
        )

        videos = Video.objects.last_24h()

        self.assertTrue(video_just_now in videos)
        self.assertTrue(video_last_24h in videos)
        self.assertTrue(video_older_than_24h not in videos)

    def test_last_week_videos(self):
        last_week = timezone.now() - datetime.timedelta(days=7)
        older_than_week = last_week - datetime.timedelta(minutes=1)

        video_last_week = baker.make(Video, published_date=last_week)
        older_than_week_video = baker.make(Video, published_date=older_than_week)

        videos = Video.objects.last_week()

        self.assertTrue(video_last_week in videos)
        self.assertTrue(older_than_week_video not in videos)

    def test_for_categories_videos(self):
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

    def test_last_24h_for_categories_videos(self):
        category_1 = baker.make(Category)
        channel_1 = baker.make(Channel)
        category_1.channels.add(channel_1)

        last_24h = timezone.now() - datetime.timedelta(hours=24)
        older_than_24h = last_24h - datetime.timedelta(minutes=1)

        video_1 = baker.make(Video, channel=channel_1, published_date=last_24h)
        video_2 = baker.make(Video, channel=channel_1, published_date=last_24h)
        video_3 = baker.make(Video, channel=channel_1, published_date=older_than_24h)
        video_4 = baker.make(Video, channel=channel_1, published_date=older_than_24h)

        videos = Video.objects.last_24h().for_categories([category_1])

        self.assertTrue(video_1 in videos)
        self.assertTrue(video_2 in videos)
        self.assertTrue(video_3 not in videos)
        self.assertTrue(video_4 not in videos)

    def test_for_categories_last_24h_videos(self):
        category_1 = baker.make(Category)
        channel_1 = baker.make(Channel)
        category_1.channels.add(channel_1)

        last_24h = timezone.now() - datetime.timedelta(hours=24)
        older_than_24h = last_24h - datetime.timedelta(minutes=1)

        video_1 = baker.make(Video, channel=channel_1, published_date=last_24h)
        video_2 = baker.make(Video, channel=channel_1, published_date=last_24h)
        video_3 = baker.make(Video, channel=channel_1, published_date=older_than_24h)
        video_4 = baker.make(Video, channel=channel_1, published_date=older_than_24h)

        videos = Video.objects.for_categories([category_1]).last_24h()

        self.assertTrue(video_1 in videos)
        self.assertTrue(video_2 in videos)
        self.assertTrue(video_3 not in videos)
        self.assertTrue(video_4 not in videos)

    def test_last_week_for_categories_videos(self):
        category_1 = baker.make(Category)
        channel_1 = baker.make(Channel)
        category_1.channels.add(channel_1)

        last_week = timezone.now() - datetime.timedelta(days=7)
        older_than_week = last_week - datetime.timedelta(minutes=1)

        video_1 = baker.make(Video, channel=channel_1, published_date=last_week)
        video_2 = baker.make(Video, channel=channel_1, published_date=last_week)
        video_3 = baker.make(Video, channel=channel_1, published_date=older_than_week)
        video_4 = baker.make(Video, channel=channel_1, published_date=older_than_week)

        videos = Video.objects.last_week().for_categories([category_1])

        self.assertTrue(video_1 in videos)
        self.assertTrue(video_2 in videos)
        self.assertTrue(video_3 not in videos)
        self.assertTrue(video_4 not in videos)

    def test_for_categories_last_week_videos(self):
        category_1 = baker.make(Category)
        channel_1 = baker.make(Channel)
        category_1.channels.add(channel_1)

        last_week = timezone.now() - datetime.timedelta(days=7)
        older_than_week = last_week - datetime.timedelta(minutes=1)

        video_1 = baker.make(Video, channel=channel_1, published_date=last_week)
        video_2 = baker.make(Video, channel=channel_1, published_date=last_week)
        video_3 = baker.make(Video, channel=channel_1, published_date=older_than_week)
        video_4 = baker.make(Video, channel=channel_1, published_date=older_than_week)

        videos = Video.objects.for_categories([category_1]).last_week()

        self.assertTrue(video_1 in videos)
        self.assertTrue(video_2 in videos)
        self.assertTrue(video_3 not in videos)
        self.assertTrue(video_4 not in videos)
