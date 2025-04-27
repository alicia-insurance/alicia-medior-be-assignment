from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class CreateShortUrlRateAnonThrottle(AnonRateThrottle):
    scope = 'create_short_url_for_anon'

class RedirectRateAnonThrottle(AnonRateThrottle):
    scope = 'redirect_for_anon'

class CreateShortUrlRateUserThrottle(UserRateThrottle):
    scope = 'create_short_url_for_user'

class RedirectRateUserThrottle(UserRateThrottle):
    scope = 'redirect_for_user'