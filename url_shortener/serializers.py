from rest_framework import serializers
from url_shortener.models import ShortURL
from url_shortener.utils import encode_id
from urllib.parse import urlparse


class ShortURLSerializer(serializers.ModelSerializer):
    short_code = serializers.SerializerMethodField()

    class Meta:
        model = ShortURL
        fields = ["id", "original_url", "short_code"]

    def get_short_code(self, obj):
        return encode_id(obj.id)

    def validate_original_url(self, value):
        parsed = urlparse(value)
        if parsed.scheme not in ["https"]:
            raise serializers.ValidationError("URL scheme must be https.")

        dangerous_schemes = ["javascript", "data", "file", "vbscript"]
        if parsed.scheme.lower() in dangerous_schemes:
            raise serializers.ValidationError(
                f"URL scheme '{parsed.scheme}' is not allowed."
            )

        return value


class ShortURLAccessCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortURL
        fields = ["access_count"]
