from django.contrib import admin
from .models import ShortURL


@admin.register(ShortURL)
class ShortURLAdmin(admin.ModelAdmin):
    list_display = (
        'short_code',
        'original_url',
        'access_count',
        'created_at',
        'expires_at',
        'custom'
    )
    search_fields = ('short_code', 'original_url')
    list_filter = ('custom', 'created_at', 'expires_at')
