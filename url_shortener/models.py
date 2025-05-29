"""
Models for URL Shortener.

Defines ShortURL model with robust indexing, expiry, and scalability in mind.
"""
from django.db import models
from django.utils import timezone


class ShortURL(models.Model):
    """
    Maps a long/original URL to a short code, with access counting and expiry.

    Attributes:
        original_url (str): The long URL to shorten.
        short_code (str): The unique code for redirection.
        access_count (int): How many times this URL was accessed.
        created_at (datetime): Creation timestamp.
        expires_at (datetime): Optional expiry date.
        custom (bool): True if user provided the code.
    """

    original_url = models.URLField()
    short_code = models.CharField(max_length=16, unique=True)
    access_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    custom = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["short_code"]),
            models.Index(fields=["created_at"]),
        ]
        ordering = ["-created_at"]
        verbose_name = "Shortened URL"
        verbose_name_plural = "Shortened URLs"

    def is_expired(self):
        """Returns True if this URL is expired (now > expires_at)."""
        return self.expires_at and timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.short_code} ({'custom' if self.custom else 'auto'})"
