from django.db import models
from .constants.messages import LABELS

class ShortURL(models.Model):
    original_url = models.URLField(max_length=2048)  # Standard max URL length
    short_alias = models.CharField(max_length=10, unique=True)
    access_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_custom_url = models.BooleanField(default=False)
    last_accessed = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.short_alias} -> {self.original_url}"

    class Meta:
        verbose_name = LABELS['LBL_SHORT_URL']
        verbose_name_plural = LABELS['LBL_SHORT_URLS']