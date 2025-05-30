from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

import url_shortener.views as url_shortner_views

schema_view = get_schema_view(
    openapi.Info(
        title="URL Shortener API",
        default_version="v1",
        description="API for shortening URLs, redirecting, and statistics",
        contact=openapi.Contact(email="your@email.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


swagger_urls = [
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("swagger.json", schema_view.without_ui(cache_timeout=0), name="schema-json"),
]


url_shortner_urls = [
    path(
        "short/<str:short_code>/",
        url_shortner_views.RedirectView.as_view(),
        name="redirect_url",
    ),
]


urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("api/", include("url_shortener.urls")),
    ]
    + url_shortner_urls
    + swagger_urls
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
