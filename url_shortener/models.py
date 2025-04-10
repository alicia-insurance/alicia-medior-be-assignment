from django.db import models
from django.core.validators import URLValidator
from django.utils.crypto import get_random_string
from django.utils import timezone
from .validators import validate_url

class ShortenedURL(models.Model):
    """
    Model representing a shortened URL
    
    Attributes:
    - original_url: The original long URL
    - short_code: The generated short code (6 characters)
    - created_at: When the URL was shortened
    - access_count: How many times the short URL has been accessed
    """
    original_url = models.CharField(
        max_length=2000,
        validators=[validate_url],
        help_text="The original URL to be shortened"
    )
    short_code = models.CharField(
        max_length=10,
        unique=True,
        help_text="The generated short code for the URL"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the URL was shortened"
    )
    access_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of times the short URL has been accessed"
    )
    
    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = self.generate_short_code()
        super().save(*args, **kwargs)
    
    def generate_short_code(self):
        """Generate a random 6-character short code"""
        code = get_random_string(length=6)
        while ShortenedURL.objects.filter(short_code=code).exists():
            code = get_random_string(length=6)
        return code
    
    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"