import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from channels.models import Category, Channel, Feed, Video


class ChannelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="username", password="password")

    def test_saving_new_channel(self):
        channel = Channel(
            title="Channel Title",
            url="https://www.youtube.com/channel/UCsn8UgBuRxGGqKmrAy5d3gA",
        )
        channel.save()

        saved_channels = Channel.objects.all()
        self.assertEqual(saved_channels.count(), 1)

    def test_channel_repr(self):
        channel = Channel.objects.create(
            title="Channel Title",
            url="https://www.youtube.com/channel/UCsn8UgBuRxGGqKmrAy5d3gA",
        )
        self.assertEqual(repr(channel), f"<Channel: {channel.title}>")

    def test_create_channel_feed_url_on_creation(self):
        channel = Channel.objects.create(
            title="Channel Title",
            url="https://www.youtube.com/channel/UCsn8UgBuRxGGqKmrAy5d3gA",
        )
        self.assertEqual(
            channel.feed_url,
            f"{settings.BASE_YOUTUBE_FEED_URL}?channel_id=UCsn8UgBuRxGGqKmrAy5d3gA",
        )

    def test_create_user_channel_feed_url_on_creation(self):
        channel = Channel.objects.create(
            title="Channel Title", url="https://www.youtube.com/user/arduinoteam",
        )
        self.assertEqual(
            channel.feed_url, f"{settings.BASE_YOUTUBE_FEED_URL}?user=arduinoteam",
        )

    def test_channel_searchable_by_video(self):
        channel = Channel.objects.create(
            title="Channel Title",
            url="https://www.youtube.com/channel/UCsn8UgBuRxGGqKmrAy5d3gA",
        )

        published_date = datetime.datetime(2020, 6, 12, 12, 38, 30)
        video = Video.objects.create(
            url="https://www.youtube.com/watch?v=UiFvgk0W3f8",
            title="LHC Convida : Gedeane Kenshima [wearables e Eletrônica, como começar?] #FiqueEmCasa",
            channel=channel,
            thumbnail_image="https://i2.ytimg.com/vi/UiFvgk0W3f8/hqdefault.jpg",
            published_date=published_date,
        )

        channels = Channel.objects.filter(video__title=video.title)
        self.assertTrue(channel in channels)

    def test_channel_searchable_by_category(self):
        category = Category.objects.create(
            title="Category Title", public=True, user=self.user,
        )
        channel = Channel.objects.create(
            title="Channel Title",
            url="https://www.youtube.com/channel/UCsn8UgBuRxGGqKmrAy5d3gA",
        )
        category.channels.add(channel)

        channels = Channel.objects.filter(categories__title=category.title)
        self.assertTrue(channel in channels)


class VideoTestCase(TestCase):
    def setUp(self):
        self.channel = Channel.objects.create(
            title="Laboratório Hacker de Campinas",
            url="https://www.youtube.com/channel/UCE4lrMOsEM6jSQvgvSdzZUA",
        )

    def test_saving_new_video(self):
        published_date = datetime.datetime(2020, 6, 12, 12, 38, 30)
        video = Video(
            url="https://www.youtube.com/watch?v=UiFvgk0W3f8",
            title="LHC Convida : Gedeane Kenshima [wearables e Eletrônica, como começar?] #FiqueEmCasa",
            channel=self.channel,
            thumbnail_image="https://i2.ytimg.com/vi/UiFvgk0W3f8/hqdefault.jpg",
            published_date=published_date,
        )
        video.save()

        saved_videos = Video.objects.all()
        self.assertEqual(saved_videos.count(), 1)

    def test_video_repr(self):
        published_date = datetime.datetime(2020, 6, 12, 12, 38, 30)
        video = Video.objects.create(
            url="https://www.youtube.com/watch?v=UiFvgk0W3f8",
            title="LHC Convida : Gedeane Kenshima [wearables e Eletrônica, como começar?] #FiqueEmCasa",
            channel=self.channel,
            thumbnail_image="https://i2.ytimg.com/vi/UiFvgk0W3f8/hqdefault.jpg",
            published_date=published_date,
        )

        self.assertEqual(repr(video), f"<Video: {video.title}>")

    def test_video_accessible_to_channel(self):
        published_date = datetime.datetime(2020, 6, 12, 12, 38, 30)
        video = Video.objects.create(
            url="https://www.youtube.com/watch?v=UiFvgk0W3f8",
            title="LHC Convida : Gedeane Kenshima [wearables e Eletrônica, como começar?] #FiqueEmCasa",
            channel=self.channel,
            thumbnail_image="https://i2.ytimg.com/vi/UiFvgk0W3f8/hqdefault.jpg",
            published_date=published_date,
        )

        self.assertTrue(video in self.channel.videos.all())


class FeedTestCase(TestCase):
    def setUp(self):
        self.channel = Channel.objects.create(
            title="Laboratório Hacker de Campinas",
            url="https://www.youtube.com/channel/UCE4lrMOsEM6jSQvgvSdzZUA",
        )

        published_date = datetime.datetime(2020, 6, 12, 12, 38, 30)
        self.video = Video.objects.create(
            url="https://www.youtube.com/watch?v=UiFvgk0W3f8",
            title="LHC Convida : Gedeane Kenshima [wearables e Eletrônica, como começar?] #FiqueEmCasa",
            channel=self.channel,
            thumbnail_image="https://i2.ytimg.com/vi/UiFvgk0W3f8/hqdefault.jpg",
            published_date=published_date,
        )

    def test_saving_new_feed(self):
        feed_content = (
            "<entry><content>Content collected from YouTube RSS feed</content></entry>"
        )
        feed = Feed(feed=feed_content, video=self.video)
        feed.save()

        saved_feeds = Feed.objects.all()
        self.assertEqual(saved_feeds.count(), 1)

    def test_feed_accessible_to_video(self):
        feed_content = (
            "<entry><content>Content collected from YouTube RSS feed</content></entry>"
        )
        feed = Feed(feed=feed_content, video=self.video)
        feed.save()

        self.assertEqual(self.video.feed, feed)


class CategoryTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="username", password="password")

    def test_saving_new_category(self):
        category = Category(title="Category Title", public=True, user=self.user,)
        category.save()
        saved_categories = Category.objects.all()
        self.assertEqual(saved_categories.count(), 1)

    def test_category_repr(self):
        category = Category.objects.create(
            title="Category Title", public=True, user=self.user,
        )
        self.assertEqual(repr(category), f"<Category: {category.title}>")

    def test_new_category_create_automatic_slug(self):
        category = Category.objects.create(
            title="Category Title", public=True, user=self.user,
        )
        self.assertEqual(category.slug, "category-title")

    def test_new_category_is_not_public_by_default(self):
        category = Category.objects.create(title="Category Title", user=self.user,)
        self.assertFalse(category.public)

    def test_channel_accessible_to_category(self):
        category = Category.objects.create(
            title="Category Title", public=True, user=self.user,
        )
        channel = Channel.objects.create(
            title="Channel Title",
            url="https://www.youtube.com/channel/UCsn8UgBuRxGGqKmrAy5d3gA",
        )
        category.channels.add(channel)

        self.assertTrue(channel in category.channels.all())

    def test_category_title_unique_to_user(self):
        category = Category.objects.create(title="Category Title", user=self.user,)

        with self.assertRaises(ValidationError):
            category_2 = Category(title="Category Title", user=self.user,)
            category_2.full_clean()

    def test_category_title_can_be_used_by_more_than_one_user(self):
        category = Category.objects.create(title="Category Title", user=self.user,)

        try:
            user_2 = User.objects.create(username="username2", password="password")
            category_2 = Category(title="Category Title", user=user_2)
            category_2.save()
            category_2.full_clean()
        except ValidationError:
            self.fail("Validation error should not be raised.")
