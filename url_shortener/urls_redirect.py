from django.urls import path
from . import views

urlpatterns = [
    path(
        "short/<str:short_code>/",
        views.RedirectShortURLView.as_view(),
        name="redirect-short-url",
    ),
]
