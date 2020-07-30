from django.urls import path

from channels import views

app_name = "channels"
urlpatterns = [
    path("<username>/", views.user_details, name="user_details"),
    path("<username>/<slug>/", views.category_details, name="category_details"),
    path("channel/", views.add_channel, name="add_channel"),
]
