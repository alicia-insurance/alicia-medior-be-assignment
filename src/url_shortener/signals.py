from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import ShortenedURL


def clear_stats_cache(short_code: str):
    """
    Helper function to clear cached statistics for a specific short URL.

    Args:
        short_code (str): The unique short code of the URL.
    """
    cache_key = f"views.decorators.cache.cache_page.stats_view.{short_code}"
    cache.delete(cache_key)


@receiver(post_save, sender=ShortenedURL)
@receiver(post_delete, sender=ShortenedURL)
def invalidate_stats_cache(sender, instance, **kwargs):
    """
    Clears cached stats view whenever a ShortenedURL instance is saved or deleted.

    Args:
        sender (type): The model class sending the signal.
        instance (ShortenedURL): The specific instance that was saved or deleted.
        **kwargs: Additional keyword arguments.
    """
    clear_stats_cache(instance.short_code)
