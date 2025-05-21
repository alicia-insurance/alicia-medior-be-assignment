from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from ..config import REDIRECT_RATE, SHORTURL_CREATE_RATE, SHORTURL_STATS_RATE

class ShortURLCreateThrottle(UserRateThrottle):
    rate = f'{SHORTURL_CREATE_RATE}/day'
    scope = 'short_url_create'

class URLStatsThrottle(UserRateThrottle):
    rate = f'{SHORTURL_STATS_RATE}/day'
    scope = 'stats'

class RedirectThrottle(AnonRateThrottle):
    rate = f'{REDIRECT_RATE}/hour'
    scope = 'redirect'