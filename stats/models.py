from django.db import models
from url_shortener.models import ShortenUrl

class RedirectCount(models.Model):
    shorten_url = models.ForeignKey(ShortenUrl, on_delete=models.CASCADE)
    redirect_count = models.IntegerField(default=0)