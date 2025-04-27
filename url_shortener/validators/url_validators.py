from django.conf import settings
from urllib.parse import urlparse
from rest_framework import serializers

def validate_url(value):
    """Validate the URL before accepting it."""

    # Check for minimum length
    if len(value) < settings.URL_MIN_LENGTH:
        raise serializers.ValidationError("URL is too short")
    
    # Check for maximum length
    if len(value) > settings.URL_MAX_LENGTH:
        raise serializers.ValidationError("URL is too long")
    
    # Check for protocols
    if not value.startswith(('http://', 'https://')):
        raise serializers.ValidationError("URL must begin with http:// or https://")

    # Blacklist check. added a static list for demostrations.
    # It needs a seperate server to perform this action.
    domain = urlparse(value).netloc
    blacklist = ['malicious-site.com', 'spam.com']
    if domain in blacklist:
        raise serializers.ValidationError(f"Domain {domain} is not allowed")
    
    return value