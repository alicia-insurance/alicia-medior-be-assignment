from django.db import models

from project import settings

class ShortenedURL(models.Model):
    """
    Model to represent a shortened URL and track the original URL, 
    its short code, custom alias (if any), and access count.
    """
    original_url = models.URLField(verbose_name="Original URL")
    short_code = models.CharField(max_length=10, unique=True, verbose_name="Shortened Code")
    custom_alias = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name="Custom Alias")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    access_count = models.PositiveIntegerField(default=0, verbose_name="Access Count")

    def get_short_url(self):
        """Returns the full short URL using either the custom alias or the short code."""
        base_url = settings.BASE_URL
        return f"{base_url}/api/short/{self.custom_alias or self.short_code}"

    def increment_access_count(self):
        """Increments the access count when the link is visited"""
        self.access_count += 1
        self.save(update_fields=["access_count"])

    def __str__(self):
        return f"{self.original_url} -> {self.get_short_url()}"
