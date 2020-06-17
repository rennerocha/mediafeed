from django.contrib import admin

from channels.models import Channel, Video, Category, Feed


admin.site.register(Category)
admin.site.register(Feed)
admin.site.register(Channel)
admin.site.register(Video)
