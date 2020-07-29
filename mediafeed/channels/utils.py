import re
from urllib.parse import urlencode

import requests
from django.conf import settings
from parsel import Selector


def get_channel_title(url):
    response = requests.get(url)

    if response.status_code == 200:
        selector = Selector(response.content.decode("utf-8"))
        channel_title = selector.xpath("//meta[@itemprop='name']/@content").get()
        return channel_title


def get_channel_feed_url(url):
    match = re.search(r"user\/(?P<user_id>.*)|channel\/(?P<channel_id>.*)", url)
    if match:
        match_dict = match.groupdict()
        user_id = match_dict.get("user_id")
        if user_id is not None:
            params = {"user": user_id}

        channel_id = match_dict.get("channel_id")
        if channel_id is not None:
            params = {"channel_id": channel_id}

        params = urlencode(params)
        feed_url = f"{settings.BASE_YOUTUBE_FEED_URL}?{params}"
        return feed_url
