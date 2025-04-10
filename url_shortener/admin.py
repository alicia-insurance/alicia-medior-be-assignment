from django.contrib import admin
from .models import ShortenedURL

@admin.register(ShortenedURL)
class ShortenedURLAdmin(admin.ModelAdmin):
    list_display = ('short_code', 'truncated_url', 'access_count', 'created_at')
    search_fields = ('original_url', 'short_code')
    list_filter = ('created_at',)
    readonly_fields = ('access_count', 'created_at')
    
    def truncated_url(self, obj):
        return (obj.original_url[:50] + '...') if len(obj.original_url) > 50 else obj.original_url
    truncated_url.short_description = 'Original URL'