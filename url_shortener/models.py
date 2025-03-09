import hashlib
import time

from django.db import models


def generate_short_code(url):
    """Generate the short code for the URL"""

    timestamp = str(int(time.time()))
    combined_string = url + timestamp
    hash_object = hashlib.sha256(combined_string.encode())
    hash_hex = hash_object.hexdigest()

    short_code = hash_hex[:6]

    counter = 1
    while ShortenedUrl.objects.filter(short_code=short_code).exists():
        short_code = hash_hex[:5] + str(counter)
        counter += 1

    return short_code


class ShortenedUrl(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="urls")
    created_at = models.DateTimeField(auto_now_add=True)
    original_url = models.URLField(unique=False, max_length=2048)
    short_code = models.CharField(max_length=10, unique=True, blank=True)
    access_count = models.PositiveIntegerField(default=0)
    last_accessed = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = generate_short_code(self.original_url)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"

class User(models.Model):
    id = models.UUIDField(primary_key=True)
    email = models.EmailField()
    first_name = models.CharField()
    last_name = models.CharField()