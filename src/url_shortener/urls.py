from django.urls import path

from .views import RedirectView, ShortenURLView, StatsView

app_name = "url_shortener"

urlpatterns = [
    path("shorten/", ShortenURLView.as_view(), name="shorten_url"),
    path("stats/<str:short_code>/", StatsView.as_view(), name="url_stats"),
    path("short/<str:short_code>/", RedirectView.as_view(), name="redirect_url"),
]
