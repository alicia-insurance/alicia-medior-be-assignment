from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/", include("url_shortener.urls")),
]
