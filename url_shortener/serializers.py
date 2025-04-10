from rest_framework import serializers
from .models import ShortenedURL
from .validators import validate_url
from django.utils import timezone

class ShortenedURLSerializer(serializers.ModelSerializer):
    """
    Serializer for ShortenedURL model
    
    Fields:
    - original_url: The original long URL to be shortened (required)
    - short_code: The generated short code (read-only)
    """
    original_url = serializers.CharField(
        max_length=2000,
        validators=[validate_url],
        help_text="The original URL to be shortened"
    )
    
    class Meta:
        model = ShortenedURL
        fields = ['original_url', 'short_code', 'access_count', 'created_at']
        read_only_fields = ['short_code', 'access_count', 'created_at']
        extra_kwargs = {
            'original_url': {
                'required': True,
                'allow_blank': False
            }
        }
    
    def validate_original_url(self, value):
        """Additional validation at serializer level"""
        validate_url(value)
        return value