import random
import string
from django.db import models

class ShortURL(models.Model):
    original_url = models.URLField(null=False, blank=False, help_text="The original URL to be shortened.")
    short_alias = models.CharField(max_length=9, unique=True, null=False, blank=False, help_text="Custom short alias for the URL, max 9 characters.")
    access_count = models.PositiveIntegerField(default=0, help_text="Number of times the short URL has been accessed.") 
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the short URL was created.") 
    is_active = models.BooleanField(default=True, help_text="Indicates if the short URL is active or not.")

    def __str__(self):
        return f"{self.short_alias} -> {self.original_url}"
    
    def increment_access_count(self):
        self.access_count += 1
        self.save(update_fields=['access_count'])
    
    def deactivate(self):
        self.is_active = False
        self.save(update_fields=['is_active'])
        
    def activate(self):
        self.is_active = True
        self.save(update_fields=['is_active'])
    
    @classmethod
    def generate_short_alias(cls, length=8, version='v1'):
        strategies = {
            'v1': cls._algorithm_v1,
        }
        if version not in strategies:
            raise NotImplementedError(f"Short Code generation for version '{version}' is not implemented.")
        return strategies[version](length)

    
    @staticmethod
    def _algorithm_v1(length):
        # just a simple random string generation for now
        # security and collision handling can be improved later
        chars = string.digits + string.ascii_lowercase + string.ascii_uppercase
        while True:
            alias = ''.join(random.choices(chars, k=length))
            if not ShortURL.objects.filter(short_alias=alias).exists():
                return alias
        
    