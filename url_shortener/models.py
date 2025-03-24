from django.db import models
import string
import random


class ShortURL(models.Model):
    original_url = models.URLField()
    short_code = models.CharField(max_length=10, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    visit_count = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = ShortURL.generate_short_code()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_short_code(length=6):
        characters = string.ascii_letters + string.digits
        while True:
            short_code = ''.join(random.choices(characters, k=length))
            if not ShortURL.objects.filter(short_code=short_code).exists():
                return short_code

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"