from django.urls import path
from .views import RedirectCountView


urlpatterns = [
    path('<str:short_code>/', RedirectCountView.as_view(), name="stats_url"),
]