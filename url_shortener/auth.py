from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get('X-API-Key')
        expected_key = settings.API_KEY

        if not api_key:
            raise AuthenticationFailed('API key missing! Please provide a valid API key in the request headers using "X-API-Key".')

        if api_key != expected_key:
            raise AuthenticationFailed('Invalid API key! Please check your API key and try again.')

        return (None, None)  # No user associated, just auth