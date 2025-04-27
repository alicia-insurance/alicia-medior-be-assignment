from django.contrib import admin
from django.urls import include, path, re_path
from common_views.not_implemented import NotImplementedView
from url_shortener.views.redirect_url import RedirectToOriginalUrlView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('short/<str:short_code>/', RedirectToOriginalUrlView.as_view(), name="redirect_to_original"),
    path("stats/", include("stats.urls")),
    path("api/", include("url_shortener.urls")),
    re_path(r'^.*$', NotImplementedView.as_view()),
]
