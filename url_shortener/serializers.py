from rest_framework import serializers
from .models import ShortURL

class ShortURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortURL
        fields = ['original_url', 'short_code', 'created_at', 'access_count']
        read_only_fields = ['short_code', 'created_at', 'access_count']
