from django.urls import path, include
from . import views

urlpatterns = [
    path("shorten/", views.URLShortenView.as_view(), name="url-create"),
    path(
        "short/<str:short_url_key>",
        views.OriginalURLView.as_view(),
        name="url-redirect",
    ),
    path(
        "stats/<str:short_url_key>/",
        views.URLStatsView.as_view(),
        name="url-stats",
    ),
    path("api-auth/", include("rest_framework.urls")),
]
