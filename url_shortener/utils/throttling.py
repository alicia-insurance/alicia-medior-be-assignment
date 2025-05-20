from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class ShortURLCreateThrottle(UserRateThrottle):
    rate = '50/day'
    scope = 'short_url_create'

class RedirectThrottle(AnonRateThrottle):
    rate = '200/hour'
    scope = 'redirect'