from .models import RedirectCount
from url_shortener.models import ShortenUrl
from .redirect_counter import flush_counts

def save_request_counts():
    counts = flush_counts()
    for shorten_url, count in counts.items():
        shorten_url_obj = ShortenUrl.objects.get(short_code=shorten_url)
        stat, _ = RedirectCount.objects.get_or_create(shorten_url=shorten_url_obj)
        stat.redirect_count += count
        stat.save()