import datetime

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from channels.models import Category, Video


def category_details(request, username, slug):
    if request.user.is_authenticated:
        category = get_object_or_404(Category, slug=slug, user=request.user)
    else:
        user = get_object_or_404(User, username=username)
        category = get_object_or_404(Category, slug=slug, user=user, public=True)

    period = request.GET.get("period", "last_24h")
    video_by_period = {
        "all": Video.objects.all(),
        "week": Video.objects.last_week(),
        "last_24h": Video.objects.last_24h(),
    }
    videos = video_by_period.get(period, [])
    context = {"videos": list(videos)}

    return render(request, "base.html", context=context)
