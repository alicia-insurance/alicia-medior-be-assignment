from rest_framework import serializers
from .models import URL, URLAccessLog

class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields = ['original_url', 'short_code', 'custom_code', 'visit_count', 'created_at']

class URLAccessLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = URLAccessLog
        fields = ['ip_address', 'user_agent', 'location', 'accessed_at']