from django.urls import path, re_path
from .views.shorten_url import CreateShortenUrlView
from common_views.not_implemented import NotImplementedView

urlpatterns = [
    path('shorten/', CreateShortenUrlView.as_view(), name="create_short_url"),    
]