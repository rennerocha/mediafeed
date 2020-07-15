import datetime

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from channels.models import Category, Video


def category_details(request, username, slug):
    user = get_object_or_404(User, username=username)
    if request.user.is_authenticated and user == request.user:
        category = get_object_or_404(Category, slug=slug, user=user)
    else:
        category = get_object_or_404(Category, slug=slug, user=user, public=True)

    videos_of_category = Video.objects.for_categories([category])

    period = request.GET.get("period", "last_24h")
    video_by_period = {
        "all": videos_of_category.all(),
        "week": videos_of_category.last_week(),
        "last_24h": videos_of_category.last_24h(),
    }
    videos = video_by_period.get(period, []).order_by("-published_date")

    # TODO - These lines needs to be have tests to ensure the context is correct
    period_labels = {"all": "All", "week": "This Week", "last_24h": "Last 24h"}
    selected_period = period_labels[period]
    ########

    context = {
        "category": category,
        "videos": list(videos),
        "selected_period": selected_period,
    }

    return render(request, "category_details.html", context=context)
