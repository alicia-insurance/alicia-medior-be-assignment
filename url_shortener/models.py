
"""
This module contains the models for the URL shortener application.
It includes the User and ShortenUrl Stat models.
Kept the models in the same file for simplicity.
"""

from django.db import models
from .utils import generate_unique_shortcode
from django.conf import settings


class ShortenUrl(models.Model):
    short_code = models.CharField(max_length=10, unique=True, blank=True)
    original_url = models.URLField(unique=False, max_length=settings.URL_MAX_LENGTH)
    created_at = models.DateTimeField(auto_now_add=True)
    is_banned = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = generate_unique_shortcode(self.original_url, ShortenUrl)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Short code {self.short_code} is mapped to {self.original_url}"
    
    # Adding indexes can improve the performance
    # But in this case, the implicit index from the
    # uniqueness constraint is already providing the
    # performance benefits. Hence commented out.
    # class Meta:
    #     indexes = [
    #         models.Index(fields=['short_code']),
    #     ]

