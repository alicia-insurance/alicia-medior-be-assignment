from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import ShortURL

class ShortURLSerializer(serializers.ModelSerializer):
    custom_alias = serializers.CharField(
        source="short_alias", required=False, allow_blank=True, max_length=8, help_text="Custom short alias for the URL, max 8 characters."
    )

    class Meta:
        model = ShortURL
        fields = ["original_url", "custom_alias", "created_at", "access_count", "is_active"]
        read_only_fields = ["created_at", "access_count", "is_active"]

    def validate_custom_alias(self, value):
        if value and ShortURL.objects.filter(short_alias=value).exists():
            raise serializers.ValidationError("This custom alias is already taken.")
        return value

    def validate_original_url(self, value):
        validate_url = URLValidator()
        try:
            validate_url(value)
        except ValidationError:
            raise serializers.ValidationError("Please provide a valid URL.")
        return value