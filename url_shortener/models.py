from django.db import models
from core.models import TimeStampedModel


class ShortURL(TimeStampedModel):
    original_url = models.URLField(max_length=2000)
    access_count = models.PositiveIntegerField(default=0)

    def increment_access_count(self):
        ShortURL.objects.filter(pk=self.pk).update(
            access_count=models.F("access_count") + 1
        )
        self.refresh_from_db(fields=["access_count"])
