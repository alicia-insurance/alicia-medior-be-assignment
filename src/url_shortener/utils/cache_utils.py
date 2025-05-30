from django.core.cache import cache
from django.urls import reverse


def clear_stats_cache(short_code: str):
    """
    Clears the cached response for the StatsView of a specific short_code.
    """
    url = reverse("url_shortener:url_stats", args=[short_code])
    cache_key = f"views.decorators.cache.cache_page.{url}"
    cache.delete(cache_key)
