from django.db import models

class URL(models.Model):
    """
    Represents a shortened URL, storing information about the original URL,
    short code, and visit statistics.
    """
    original_url = models.URLField(max_length=2000)
    short_code = models.CharField(max_length=50, unique=True, db_index=True)
    custom_code = models.CharField(max_length=50, blank=True, null=True, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    visit_count = models.PositiveIntegerField(default=0)
    last_accessed = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['short_code']),
            models.Index(fields=['custom_code']),
        ]

class URLAccessLog(models.Model):
    """
    Logs each access to a shortened URL, capturing details such as IP address,
    user agent, and location.
    """
    url = models.ForeignKey(URL, related_name='access_logs', on_delete=models.CASCADE)
    accessed_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Access log for {self.url.short_code}"
