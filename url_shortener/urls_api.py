from django.urls import path
from . import views

urlpatterns = [
    path("<str:version>/shorten/", views.ShortenURLView.as_view(), name="shorten-url"),
    path(
        "<str:version>/stats/<str:short_code>/",
        views.ShortURLStatsView.as_view(),
        name="short-url-stats",
    ),
]
