import datetime

from django.test import TestCase

from channels.models import Channel, Video


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
