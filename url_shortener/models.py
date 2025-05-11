from django.db import models
from django.core.validators import URLValidator


class ShortenedURL(models.Model):
    """
    Model class for url specific attributes
    """

    original_url = models.TextField(validators=[URLValidator()])
    short_url_key = models.TextField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ShortenURLAccessLog(models.Model):
    """
    Model class for shortened url access log
    """

    short_url_key = models.ForeignKey(ShortenedURL, on_delete=models.CASCADE)
    access_time = models.DateTimeField(auto_now_add=True)
