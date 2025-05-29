"""
Serializers for Shortener.

Handles input validation, security, and output formatting.
"""

from rest_framework import serializers
from .models import ShortURL
from django.utils import timezone


class ShortenURLSerializer(serializers.ModelSerializer):
    custom_short_code = serializers.CharField(
        required=False, allow_blank=True, max_length=16
    )
    expires_at = serializers.DateTimeField(required=False, allow_null=True)

    class Meta:
        model = ShortURL
        fields = ['original_url', 'custom_short_code', 'expires_at']

    def validate_original_url(self, value):
        # Prevent SSRF and malicious URLs by blocking private/local addresses
        import re
        if re.match(
            r"^https?://(localhost|127\.0\.0\.1|0\.0\.0\.0|10\.|192\.168\.|172\.)",
            value
        ):
            raise serializers.ValidationError("Private network URLs are not allowed.")
        return value

    def validate_custom_short_code(self, value):
        if value:
            if not value.isalnum():
                raise serializers.ValidationError("Short code must be alphanumeric.")
            if ShortURL.objects.filter(short_code=value).exists():
                raise serializers.ValidationError("Short code already in use.")
        return value

    def validate_expires_at(self, value):
        if value and value < timezone.now():
            raise serializers.ValidationError("Expiry must be in the future.")
        return value

    def create(self, validated_data):
        custom_code = validated_data.pop('custom_short_code', None)
        if custom_code:
            short_code = custom_code
            custom = True
        else:
            from .utils import generate_short_code
            for _ in range(10):  # Retry up to 10 times for uniqueness
                code = generate_short_code()
                if not ShortURL.objects.filter(short_code=code).exists():
                    short_code = code
                    custom = False
                    break
            else:
                raise serializers.ValidationError(
                    "Failed to generate unique code. Please try again."
                )
        obj = ShortURL.objects.create(short_code=short_code, custom=custom, **validated_data)
        return obj


class ShortenURLResponseSerializer(serializers.Serializer):
    short_url = serializers.URLField()


class ShortURLStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortURL
        fields = [
            'original_url',
            'short_code',
            'access_count',
            'created_at',
            'expires_at',
            'custom',
        ]
