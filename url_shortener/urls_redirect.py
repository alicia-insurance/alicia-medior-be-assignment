from django.urls import path
from . import views

urlpatterns_api = [
    path("<str:version>/shorten/", views.ShortenURLView.as_view(), name="shorten-url"),
    path("<str:version>/stats/<str:short_code>/", views.ShortURLStatsView.as_view(), name="short-url-stats"),
]

urlpatterns_redirect = [
    path("short/<str:short_code>/", views.RedirectShortURLView.as_view(), name="redirect-short-url"),
]

urlpatterns = urlpatterns_api + urlpatterns_redirect