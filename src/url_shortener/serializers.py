import re

from rest_framework import serializers

from .models import ShortenedURL


class ShortenURLSerializer(serializers.ModelSerializer):
    """
    Serializer for shortening URLs with optional custom short codes.

    Fields:
        original_url (str): The long URL to be shortened.
        custom_code (str, optional): User-specified custom short code (alphanumeric, hyphens, underscores).

    Validations:
        - Ensures custom_code (if provided) contains only allowed characters.
        - Ensures custom_code is unique across existing short codes.
    """

    custom_code = serializers.CharField(required=False, max_length=10)

    class Meta:
        model = ShortenedURL
        fields = ("original_url", "custom_code")

    def validate_custom_code(self, value):
        """
        Validates the custom_code field:
        - Only allows alphanumeric characters, hyphens, and underscores.
        - Checks uniqueness against existing short codes.

        Raises:
            serializers.ValidationError: If format is invalid or code already exists.

        Returns:
            str: Validated custom short code.
        """
        if not re.match(r"^[a-zA-Z0-9_-]+$", value):
            raise serializers.ValidationError(
                "Only letters, numbers, underscores, and hyphens are allowed."
            )

        if ShortenedURL.objects.filter(short_code=value).exists():
            raise serializers.ValidationError("This short code is already taken.")

        return value


class ShortenedURLResponseSerializer(serializers.ModelSerializer):
    """
    Serializer for returning URL shortening results and usage statistics.

    Fields (read-only):
        - original_url (str): The original long URL submitted by the user.
        - short_code (str): The generated or custom short code.
        - access_count (int): The number of times the short URL has been accessed.
    """

    original_url = serializers.URLField(read_only=True)
    short_code = serializers.CharField(read_only=True)
    access_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = ShortenedURL
        fields = ("original_url", "short_code", "access_count")
