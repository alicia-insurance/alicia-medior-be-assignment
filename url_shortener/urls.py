from django.urls import path
from . import views

app_name = 'url_shortener'

urlpatterns = [
    path('api/shorten/', views.shorten_url, name='shorten-url'),
    path('short/<str:short_code>/', views.redirect_to_original, name='redirect-original'),
    path('api/stats/<str:short_code>/', views.url_stats, name='url-stats'),
]