from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from urllib.parse import urlparse

def validate_url(value):
    """
    Custom URL validator that ensures:
    - Proper URL scheme (http/https)
    - Basic URL structure
    """
    if not value:
        raise ValidationError("URL is required")
    
    # Basic check for URL scheme
    if not value.startswith(('http://', 'https://')):
        raise ValidationError("URL must start with http:// or https://")
    
    # Django's built-in URL validator
    validator = URLValidator()
    validator(value)
    
    # Additional checks
    parsed = urlparse(value)
    if not parsed.netloc:  # Check domain exists
        raise ValidationError("Invalid URL - missing domain")