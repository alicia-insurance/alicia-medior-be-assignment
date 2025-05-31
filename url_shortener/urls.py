from django.urls import path
from .views import ShortenURLView, RedirectURLView, URLStatsView

urlpatterns = [
    path('shorten/', ShortenURLView.as_view(), name='shorten-url'),
    path('stats/<str:short_code>/', URLStatsView.as_view(), name='url-stats'),
    path('<str:short_code>/', RedirectURLView.as_view(), name='redirect-url'),
]
