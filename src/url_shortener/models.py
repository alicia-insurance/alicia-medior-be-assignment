from django.db import models, IntegrityError, transaction
from django.utils.crypto import get_random_string
from django.utils import timezone
import string

BASE62_CHARS = string.digits + string.ascii_letters

def generate_base62_code(length=8):
    return ''.join(get_random_string(length=1, allowed_chars=BASE62_CHARS) for _ in range(length))

class ShortenedURL(models.Model):
    """
    Model representing a shortened URL.
    Attributes:
        original_url (models.URLField): The original long URL to be shortened.
        short_code (models.CharField): Auto-generated unique short code for the shortened URL.
        access_count (models.PositiveIntegerField): Number of times the short URL was accessed.
        created_at (models.DateTimeField): Timestamp when the shortened URL was created.
        expires_at (models.DateTimeField): Optional expiration date for the short URL.
    Methods:
        save(self, *args, **kwargs) -> None:
            Saves the ShortenedURL instance, generating a unique short_code if not provided.
            Retries up to 5 times in case of short_code collisions.
        is_expired(self) -> bool:
            Returns True if the shortened URL has expired, otherwise False.
        __str__(self) -> str:
            Returns a human-readable string representation of the ShortenedURL.
        __repr__(self) -> str:
            Returns a detailed string representation of the ShortenedURL for debugging.
    """
    original_url = models.URLField(max_length=2048, help_text="The original long URL to be shortened.")
    short_code = models.CharField(max_length=10, unique=True, blank=True, help_text="Auto-generated short code.")
    access_count = models.PositiveIntegerField(default=0, help_text="Number of times the short URL was accessed.")
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True, help_text="Expiration date for the short URL.")

    objects = models.Manager()

    def save(self, *args, **kwargs):
        if self.short_code:
            return super().save(*args, **kwargs)

        for _ in range(5):
            self.short_code = generate_base62_code()
            try:
                with transaction.atomic():
                    super().save(*args, **kwargs)
                    return
            except IntegrityError:
                continue

        raise ValueError("Unable to generate a unique short code after 5 attempts.")

    def is_expired(self):
        return self.expires_at and timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.short_code} → {self.original_url}"

    def __repr__(self):
        return (
            f"ShortenedURL(original_url={self.original_url}, "
            f"short_code={self.short_code}, access_count={self.access_count})"
        )
