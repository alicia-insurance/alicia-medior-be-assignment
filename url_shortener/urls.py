from django.urls import path
from .views import ShortURLCreateAPIView, redirect_short_url, short_url_stats

urlpatterns = [
    path('api/shorten/', ShortURLCreateAPIView.as_view(), name='api-shorten'),
    path('<str:short_code>/', redirect_short_url, name='redirect'),
    path('stats/<str:short_code>/', short_url_stats, name='short-url-stats'),
]