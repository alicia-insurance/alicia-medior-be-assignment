from rest_framework import serializers
from .models import ShortURL

class ShortURLSerializer(serializers.ModelSerializer):
    custom_code = serializers.CharField(required=False, write_only=True)
    short_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ShortURL
        fields = ['id', 'original_url', 'short_code', 'access_count', 'created_at', 'custom_code', 'short_url']
        read_only_fields = ['short_code', 'access_count', 'created_at', 'short_url']

    def get_short_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f"/{obj.short_code}/")
        return f"/{obj.short_code}/"

    def validate_custom_code(self, value):
        if ShortURL.objects.filter(short_code=value).exists():
            raise serializers.ValidationError("Custom short code is already taken.")
        return value

    def create(self, validated_data):
        custom_code = validated_data.pop('custom_code', None)
        short_url = ShortURL(**validated_data)
        if custom_code:
            short_url.short_code = custom_code
        short_url.save()
        return short_url
