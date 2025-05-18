from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from url_shortener.models import ShortURL
from url_shortener.serializers import ShortURLSerializer

from django.conf import settings

class ShortenURLView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ShortURLSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        short_alias = serializer.validated_data.get("short_alias", None)
        print(f"Short alias provided: {short_alias}")
        if not short_alias:
            short_alias = ShortURL.generate_short_alias(version=request.version)
        short_url = serializer.save(short_alias=short_alias, is_active=True)
        return Response(
            {"short_url": f"{settings.SITE_DOMAIN}/short/{short_url.short_alias}/"},
            status=status.HTTP_201_CREATED
        )

class ShortURLStatsView(APIView):
    def get(self, request, short_code, *args, **kwargs):
        version = request.version
        # TODO
        # fetch the ShortURL object by short_code
        # return the short_code, access_count and created_at

        # dummy response for now
        return Response({
            "access_count": 42,
            "created_at": "2024-01-01T00:00:00Z"
        }, status=status.HTTP_200_OK)

class RedirectShortURLView(APIView):
    def get(self, request, short_code, *args, **kwargs):
        # TODO
        # fetch the ShortURL object by short_code
        # optionally, validate if the short_code is active or not
        # increment the access_count
        # redirect to the original_url
        try:
            obj = ShortURL.objects.get(short_alias=short_code)
            if not obj.is_active:
                return Response({"error": "Short code is inactive"}, status=status.HTTP_404_NOT_FOUND)
        except ShortURL.DoesNotExist:
            return Response({"error": "Short code not found"}, status=status.HTTP_404_NOT_FOUND)
        return redirect(obj.original_url)