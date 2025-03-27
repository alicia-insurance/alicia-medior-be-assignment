from rest_framework.throttling import UserRateThrottle

class URLCreationThrottle(UserRateThrottle):
    scope = 'url_creation'
