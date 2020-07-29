from unittest.mock import Mock, patch

from django.conf import settings
from django.test import TestCase

from channels.utils import get_channel_feed_url, get_channel_title

YOUTUBE_CHANNEL_CONTENT = b"""<html>
    <head>
        <meta itemprop="name" content="Channel Title">
    </head>
</html>
"""


class ChannelGetTitleTestCase(TestCase):
    def setUp(self):
        self.channel_url = "http://channel.url"
        self.patch_get = patch("channels.utils.requests.get")

        self.mock_get = self.patch_get.start()
        self.mock_get.return_value.status_code = 200

    def tearDown(self):
        self.patch_get.stop()

    def test_return_none_if_url_invalid(self):
        self.mock_get.return_value.status_code = 404

        channel_title = get_channel_title(url=self.channel_url)

        self.assertTrue(channel_title is None)

    def test_return_channel_title_of_valid_youtube_channel_url(self):
        self.mock_get.return_value.content = YOUTUBE_CHANNEL_CONTENT

        channel_title = get_channel_title(url=self.channel_url)

        self.assertTrue(channel_title == "Channel Title")

    def test_return_none_for_invalid_youtube_channel_url(self):
        self.mock_get.return_value.content = (
            b"<html><body>This is not a Youtube page</body></html>"
        )

        channel_title = get_channel_title(url=self.channel_url)

        self.assertTrue(channel_title is None)


class ChannelGetFeedURLTestCase(TestCase):
    def setUp(self):
        self.channel_url = "http://channel.url"

    def test_feed_url_from_channel_url(self):
        channel_url = "https://www.youtube.com/channel/UCsn8UgBuRxGGqKmrAy5d3gA"

        feed_url = get_channel_feed_url(channel_url)

        self.assertEqual(
            f"{settings.BASE_YOUTUBE_FEED_URL}?channel_id=UCsn8UgBuRxGGqKmrAy5d3gA",
            feed_url,
        )

    def test_feed_url_from_user_url(self):
        channel_url = "https://www.youtube.com/user/arduinoteam"

        feed_url = get_channel_feed_url(channel_url)

        self.assertEqual(
            f"{settings.BASE_YOUTUBE_FEED_URL}?user=arduinoteam", feed_url,
        )
