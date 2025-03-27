from django.core.exceptions import ValidationError
import re
from django.core.validators import URLValidator

def validate_custom_code(value):
    if not re.match("^[a-zA-Z0-9_-]+$", value):
        raise ValidationError("Custom short codes can only contain letters, digits, dashes, and underscores.")

def validate_url(value):
    url_validator = URLValidator()
    try:
        url_validator(value)
    except ValidationError:
        raise ValidationError("Invalid URL format.")