import json

import dateparser
import requests
import xmltodict
from django.core.management.base import BaseCommand, CommandError

from channels.models import Channel, Video, Feed


class Command(BaseCommand):
    help = "Sync all channels with latest videos"

    def handle(self, *args, **options):
        channels = Channel.objects.values_list("id", "channel_id")
        for id_, channel_id in channels:
            existing_videos = list(
                Video.objects.filter(channel__channel_id=channel_id).values_list(
                    "video_id", flat=True
                )
            )

            feed_url = (
                f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
            )
            response = requests.get(feed_url)
            feed = xmltodict.parse(response.text)

            latest_videos = feed["feed"]["entry"]
            for video_feed in latest_videos:
                video_id = video_feed["yt:videoId"]

                if video_id not in existing_videos:
                    video = Video.objects.create(
                        url=video_feed["link"]["@href"],
                        title=video_feed["title"],
                        channel_id=id_,
                        video_id=video_id,
                        thumbnail_image=video_feed["media:group"]["media:thumbnail"][
                            "@url"
                        ],
                        published_date=dateparser.parse(video_feed["published"]),
                    )

                    Feed.objects.create(
                        video=video, feed=json.dumps(video_feed),
                    )


# https://www.youtube.com/feeds/videos.xml?user=USERNAME
# https://www.youtube.com/feeds/videos.xml?channel_id=CHANNELID
# https://www.youtube.com/feeds/videos.xml?playlist_id=PLAYLISTID

# For Vimeo :

# https://vimeo.com/channels/CHANNELID/videos/rss
# http://vimeo.com/USERNAME/likes/rss
# http://vimeo.com/USERNAME/videos/rss
