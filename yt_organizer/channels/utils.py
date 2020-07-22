import requests
from parsel import Selector


def get_channel_title(url):
    response = requests.get(url)

    if response.status_code == 200:
        selector = Selector(response.content.decode("utf-8"))
        channel_title = selector.xpath("//meta[@itemprop='name']/@content").get()
        return channel_title
