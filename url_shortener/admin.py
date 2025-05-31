from django.contrib import admin
from .models import ShortURL

@admin.register(ShortURL)
class ShortURLAdmin(admin.ModelAdmin):
    list_display = ('original_url', 'short_code', 'access_count', 'created_at')
    search_fields = ('original_url', 'short_code')
