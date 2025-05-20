from django.urls import path
from .views import URLShortenerView, URLStatsView, URLRedirectView

urlpatterns = [
    path('shorten/', URLShortenerView.as_view(), name='shorten-url'),
    path('stats/<str:short_code>/', URLStatsView.as_view(), name='url-stats'),
    path('<str:short_code>/', URLRedirectView.as_view(), name='url-redirect'),
]