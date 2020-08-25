from django.urls import path

from core import views

app_name = "core"
urlpatterns = [
    path("profile/", views.user_profile, name="user_profile"),
]
