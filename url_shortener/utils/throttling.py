from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class ShortURLCreateThrottle(UserRateThrottle):
    scope = 'short_url_create'

class RedirectThrottle(AnonRateThrottle):
    scope = 'redirect'

class URLStatsThrottle(UserRateThrottle):
    scope = 'stats'