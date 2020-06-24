from django.core.management.base import BaseCommand, CommandError

from channels.models import Channel


class Command(BaseCommand):
    help = "Sync all channels with latest videos"

    def handle(self, *args, **options):
        channels = Channel.objects.all()
        for channel in channels:
            channel.sync_videos()
