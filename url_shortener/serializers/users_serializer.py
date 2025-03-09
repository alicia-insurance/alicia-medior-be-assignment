from rest_framework import serializers
from url_shortener.models import User


class UsersSerializer(serializers.ModelSerializer):
    total_access_count = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "total_access_count"]

    def total_access_count(self, user):
        count = sum([url.access_count for url in user.access_count])