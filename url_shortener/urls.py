from django.urls import path
from .views import URLShortenerView, URLStatsView

urlpatterns = [
    path('shorten/', URLShortenerView.as_view(), name='shorten-url'),
    path('stats/<str:short_code>/', URLStatsView.as_view(), name='url-stats'),
]