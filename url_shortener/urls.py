from django.urls import path
from .views import ShortURLCreateAPIView, redirect_short_url

urlpatterns = [
    path('api/shorten/', ShortURLCreateAPIView.as_view(), name='api-shorten'),
    path('<str:short_code>/', redirect_short_url, name='redirect'),
]