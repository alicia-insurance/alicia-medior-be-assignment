from django.urls import path

from .views import get_url_stats, redirect_url, shorten_url

urlpatterns = [
    path('shorten/', shorten_url, name='shorten_url'),  # Shorten a URL
    path(
        'short/<str:short_code>/', redirect_url, name='redirect_url'
    ),  # Redirect to the original URL
    path(
        'stats/<str:short_code>/', get_url_stats, name='url_stats'
    ),  # Get stats (Bonus)
]
