from django.contrib import admin

from channels.models import Category, Channel, Feed, Video


class VideoInline(admin.TabularInline):
    model = Video


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    inlines = [
        VideoInline,
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    readonly_fields = ("slug",)


class FeedInline(admin.TabularInline):
    model = Feed


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    inlines = [
        FeedInline,
    ]


admin.site.register(Feed)
