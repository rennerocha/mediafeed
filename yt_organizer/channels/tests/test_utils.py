from unittest.mock import Mock, patch

from django.test import TestCase

from channels.utils import get_channel_title

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
