from django.urls import path
from .views import ShortenURLView, RedirectView, StatsView

urlpatterns = [
    path('api/shorten/', ShortenURLView.as_view(), name='shorten-url'),
    path('api/stats/<str:short_code>/', StatsView.as_view(), name='url-stats'),
    path('s/<str:short_code>/', RedirectView.as_view(), name='redirect-url'),
]
