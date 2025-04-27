from rest_framework import serializers
from url_shortener.models import ShortenUrl
from url_shortener.validators.url_validators import validate_url


class CreateShortenUrlPublicSerializer(serializers.ModelSerializer):
	""" Serializer for public URL shortening API. """
	url = serializers.SerializerMethodField()
	original_url = serializers.CharField(validators=[validate_url])

	def get_url(self, obj):
		request = self.context.get('request')
		if request:
			return request.build_absolute_uri(f"/short/{obj.short_code}/")
		return f"/short/{obj.short_code}/"
	
	class Meta:
		model = ShortenUrl
		fields = [
			'short_code',
			'original_url',
			'created_at',
			'url'
		]
		read_only_fields = ['short_code', 'created_at', 'is_expired', 'is_banned']
