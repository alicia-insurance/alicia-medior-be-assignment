from rest_framework import serializers
from .models import ShortURL

class ShortURLSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()
    short_code = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = ShortURL
        fields = ['id', 'original_url', 'short_code', 'short_url', 'created_at', 'visit_count']
        read_only_fields = ['id', 'short_url', 'created_at', 'visit_count']

    def get_short_url(self, obj):
        request = self.context.get('request')
        domain = request.build_absolute_uri('/') if request else 'http://localhost:8000/'
        return f"{domain}s/{obj.short_code}/"

    def validate_short_code(self, value):
        if value:
            if ShortURL.objects.filter(short_code=value).exists():
                raise serializers.ValidationError("This short code is already taken.")
            if not value.isalnum():
                raise serializers.ValidationError("Short code must be alphanumeric.")
        return value
    
    def create(self, validated_data):
        return ShortURL.objects.create(**validated_data)    