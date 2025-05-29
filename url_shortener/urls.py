from django.urls import path
from .views import (
    ShortenURLAPIView,
    ShortURLStatsAPIView,
    ShortURLListView,
)

urlpatterns = [
    path('shorten/', ShortenURLAPIView.as_view(), name='shorten-url'),
    path('stats/<str:short_code>/', ShortURLStatsAPIView.as_view(), name='short-url-stats'),
    path('shorturls/', ShortURLListView.as_view(), name='short-url-list'),
]
