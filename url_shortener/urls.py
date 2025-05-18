from django.urls import path
from url_shortener.views import ShortenURLView, RedirectShortURLView, ShortURLStatsView

urlpatterns = [
    path("shorten/", ShortenURLView.as_view(), name="shorten-url"),
    path("short/<short_code>/", RedirectShortURLView.as_view(), name="redirect-url"),
    path(
        "short/<short_code>/stats/", ShortURLStatsView.as_view(), name="short-url-stats"
    ),
]
