from django.contrib import messages
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from channels.models import Category, Channel, Video


def category_details(request, username, slug):
    user = get_object_or_404(User, username=username)
    if request.user.is_authenticated and user == request.user:
        selected_category = get_object_or_404(Category, slug=slug, user=user)
        categories = Category.objects.filter(user=request.user).order_by("title")
    else:
        selected_category = get_object_or_404(
            Category, slug=slug, user=user, public=True
        )
        categories = Category.objects.filter(user=user, public=True).order_by("title")

    videos_of_category = Video.objects.for_categories([selected_category])

    period = request.GET.get("period", "last_24h")
    video_by_period = {
        "all": videos_of_category.all(),
        "week": videos_of_category.last_week(),
        "last_24h": videos_of_category.last_24h(),
    }
    videos = video_by_period.get(period, []).order_by("-published_date")

    context = {
        "user": user,
        "selected_category": selected_category,
        "period": period,
        "categories": categories,
        "videos": list(videos),
    }

    return render(request, "category_details.html", context=context)


def user_details(request, username):
    user = get_object_or_404(User, username=username)
    categories = []

    if request.user == user:
        ...
    else:
        categories = Category.objects.filter(user=user, public=True).order_by("title")
        if not categories:
            raise Http404()

    videos = Video.objects.for_categories(categories)

    context = {
        "categories": categories,
        "videos": videos,
    }

    return render(request, "user_details.html", context=context)


def add_channel(request):
    if request.method == "POST":
        category_id = request.POST.get("category_id")
        current_url = request.POST.get("current_url")
        channel_url = request.POST.get("url")

        channel = Channel.objects.create(url=channel_url)
        channel.sync_videos()

        messages.success(
            request, f'Channel "{channel.title}" has been successfully added.'
        )

        category = Category.objects.get(id=category_id)
        category.channels.add(channel)

        return redirect(current_url)
