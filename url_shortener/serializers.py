import random
import string
from django.db.models import Max
from rest_framework import serializers
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .models import ShortenedURL


class URLShortenerSerializer(serializers.ModelSerializer):
    """
    Serializer for POST request for URL creation
    """

    class Meta:
        model = ShortenedURL
        fields = ("original_url", "short_url_key")
        read_only_fields = ("short_url_key",)

    def validate(self, attrs):

        original_url = attrs.get("original_url")
        try:
            validator = URLValidator()
            validator(original_url)
            return attrs
        except ValidationError:
            raise serializers.ValidationError("Given URL is invalid")

    def create(self, validated_data):

        while True:
            # Generating random key for short url key
            short_url_key = "".join(
                random.choices(string.ascii_letters + string.digits, k=10)
            )
            if not ShortenedURL.objects.filter(short_url_key=short_url_key).exists():
                break

        validated_data["short_url_key"] = short_url_key
        return super().create(validated_data)


class OriginalURLSerializer(serializers.ModelSerializer):
    """
    Serializer for GET request for original URL
    """

    class Meta:
        model = ShortenedURL
        fields = ("original_url",)


class ShortenedURLStatsSerializer(serializers.ModelSerializer):
    """
    Serializer for GET request for shortened URL stats
    """

    access_count = serializers.SerializerMethodField()
    last_accessed_at = serializers.SerializerMethodField()

    class Meta:
        model = ShortenedURL
        fields = ("short_url_key", "created_at", "access_count", "last_accessed_at")

    def get_access_count(self, obj):
        return obj.shortenurlaccesslog_set.count()

    def get_last_accessed_at(self, obj):
        latest_access = obj.shortenurlaccesslog_set.aggregate(
            last_access=Max("access_time")
        )
        return latest_access["last_access"]
