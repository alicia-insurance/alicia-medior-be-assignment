from django.urls import path
from .views import ShortenURL, RedirectURL, URLStats

urlpatterns = [
    path('api/shorten/', ShortenURL.as_view(), name='shorten_url'),  # Shorten a URL
    path('short/<str:short_code>/', RedirectURL.as_view(), name='redirect_url'),  # Redirect to original URL
    path('api/stats/<str:short_code>/', URLStats.as_view(), name='url_stats'),  # Get URL stats
]
