from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("url_shortener.urls_api")), # API endpoints
    path("", include("url_shortener.urls_redirect")),  # Redirect endpoint
]
