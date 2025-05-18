from django.db import models

class ShortURL(models.Model):
    original_url = models.URLField(null=False, blank=False, help_text="The original URL to be shortened.")
    short_alias = models.CharField(max_length=9, unique=True, null=False, blank=False, help_text="Custom short alias for the URL, max 9 characters.")
    access_count = models.PositiveIntegerField(default=0, help_text="Number of times the short URL has been accessed.") 
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the short URL was created.") 
    is_active = models.BooleanField(default=True, help_text="Indicates if the short URL is active or not.")

    def __str__(self):
        return f"{self.short_alias} -> {self.original_url}"