import datetime

from django.test import TestCase
from model_bakery import baker

from channels.models import Category, Channel, Video


class VideoManagerTestCase(TestCase):
    def setUp(self):
        self.channel = Channel.objects.create(
            title="Laboratório Hacker de Campinas",
            url="https://www.youtube.com/channel/UCE4lrMOsEM6jSQvgvSdzZUA",
        )

    def test_last_24h(self):
        last_24h = datetime.datetime.now() - datetime.timedelta(hours=24)
        older_than_24h = last_24h + datetime.timedelta(seconds=1)

        video_last_24h = Video.objects.create(
            url="https://www.youtube.com/watch?v=UiFvgk0W3f8",
            title="LHC Convida : Gedeane Kenshima [wearables e Eletrônica, como começar?] #FiqueEmCasa",
            channel=self.channel,
            thumbnail_image="https://i2.ytimg.com/vi/UiFvgk0W3f8/hqdefault.jpg",
            published_date=last_24h,
        )
        older_video = Video.objects.create(
            url="https://www.youtube.com/watch?v=t_AZThnDUCU",
            title="LHC Convida: Sérgio Amadeu [Tecnologia e Política] #FiqueEmCasa",
            channel=self.channel,
            thumbnail_image="https://i1.ytimg.com/vi/t_AZThnDUCU/hqdefault.jpg",
            published_date=older_than_24h,
        )

        videos = Video.objects.last_24h()

        self.assertTrue(video_last_24h in videos)
        self.assertTrue(older_video not in videos)

    def test_last_week(self):
        last_week = datetime.datetime.now() - datetime.timedelta(days=7)
        older_than_week = last_week + datetime.timedelta(seconds=1)

        video_last_week = Video.objects.create(
            url="https://www.youtube.com/watch?v=UiFvgk0W3f8",
            title="LHC Convida : Gedeane Kenshima [wearables e Eletrônica, como começar?] #FiqueEmCasa",
            channel=self.channel,
            thumbnail_image="https://i2.ytimg.com/vi/UiFvgk0W3f8/hqdefault.jpg",
            published_date=last_week,
        )
        older_than_week_video = Video.objects.create(
            url="https://www.youtube.com/watch?v=t_AZThnDUCU",
            title="LHC Convida: Sérgio Amadeu [Tecnologia e Política] #FiqueEmCasa",
            channel=self.channel,
            thumbnail_image="https://i1.ytimg.com/vi/t_AZThnDUCU/hqdefault.jpg",
            published_date=older_than_week,
        )

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
