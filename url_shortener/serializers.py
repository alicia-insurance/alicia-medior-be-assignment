from rest_framework import serializers
from .models import ShortURL

class ShortURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortURL
        fields = ['original_url', 'short_alias', 'created_at']
        read_only_fields = ['short_alias', 'created_at']

class URLStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortURL
        fields = ['short_alias', 'original_url', 'created_at', 'access_count', 'last_accessed']
