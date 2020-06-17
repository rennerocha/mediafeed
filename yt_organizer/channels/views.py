from django.http import HttpResponse
import datetime
from django.shortcuts import render
from channels.models import Category, Video


def category_details(request, slug):
    category = Category.objects.get(slug=slug)
    channels = category.channels.all()

    last_24h = datetime.datetime.now() - datetime.timedelta(hours=24)
    videos = Video.objects.filter(published_date__gte=last_24h).order_by(
        "published_date"
    )

    return render(
        request, "category_details.html", {"category": category, "videos": videos}
    )
