from django.contrib import admin

from .models import ShortenedURL


@admin.register(ShortenedURL)
class ShortenedURLAdmin(admin.ModelAdmin):
    """
    Admin interface customization for the ShortenedURL model.
    """

    list_display = ("short_code", "original_url", "access_count", "created_at")
    list_filter = ("created_at",)
    search_fields = ("short_code", "original_url")
    readonly_fields = ("short_code", "access_count", "created_at")
    ordering = ("-created_at",)
