from rest_framework import serializers

from .models import ShortenedURL


class ShortenedURLSerializer(serializers.ModelSerializer):
    short_url = serializers.ReadOnlyField(source='get_short_url')

    class Meta:
        model = ShortenedURL
        fields = [
            "id",
            "original_url",
            "short_code",
            "custom_alias",
            "short_url",
            "created_at",
            "access_count",
        ]
        read_only_fields = ["short_code", "short_url", "created_at", "access_count"]
