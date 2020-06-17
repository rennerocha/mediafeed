from django.urls import path

from channels import views


urlpatterns = [
    path("<slug>/", views.category_details),
]
