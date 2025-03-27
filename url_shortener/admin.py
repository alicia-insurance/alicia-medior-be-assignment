from django.contrib import admin
from .models import URL

@admin.register(URL)
class URLAdmin(admin.ModelAdmin):
    list_display = ['short_code', 'original_url', 'visit_count', 'created_at']
