from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle

from django.shortcuts import redirect
from url_shortener.auth import APIKeyAuthentication
from url_shortener.models import ShortURL
from url_shortener.serializers import ShortURLSerializer

from django.conf import settings

from url_shortener.throttles import BurstRateThrottle


class ShortenURLView(APIView):
    throttle_classes = [AnonRateThrottle]
    authentication_classes = [APIKeyAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = ShortURLSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        short_alias = serializer.validated_data.get("short_alias", None)
        print(f"Short alias provided: {short_alias}")
        try:
            # If no custom alias is provided, generate a short alias
            if not short_alias:
                short_alias = ShortURL.generate_short_alias(version=request.version)
            short_url = serializer.save(short_alias=short_alias, is_active=True)
            return Response(
                {"short_url": f"{settings.SITE_DOMAIN}/short/{short_url.short_alias}/"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            print(f"Error creating short URL: {e}")
            return Response(
                {"An unexpected error occurred. Please report this to our team."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ShortURLStatsView(APIView):
    throttle_classes = [AnonRateThrottle]
    authentication_classes = [APIKeyAuthentication]

    def get(self, request, short_code, *args, **kwargs):
        try:
            print(f"Fetching stats for short code: {short_code}")
            obj = ShortURL.objects.get(short_alias=short_code)
            return Response(
                {
                    "short_code": obj.short_alias,
                    "access_count": obj.access_count,
                    "created_at": obj.created_at.strftime("%Y-%m-%d"),
                },
                status=status.HTTP_200_OK,
            )
        except ShortURL.DoesNotExist:
            print(f"Short code {short_code} not found")
            return Response(
                {"error": "Short code not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(f"Error fetching stats: {e}")
            return Response(
                {"An unexpected error occurred. Please report this to our team."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class RedirectShortURLView(APIView):
    throttle_classes = [BurstRateThrottle]
    authentication_classes = []

    def get(self, request, short_code, *args, **kwargs):
        try:
            print(f"Attempting to redirect using short code: {short_code}")
            obj = ShortURL.objects.get(short_alias=short_code)
            if not obj.is_active:
                print(f"Short code {short_code} is inactive")
                return Response(
                    {"error": "Short code is inactive"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            obj.increment_access_count()
            print(f"Redirecting to: {obj.original_url}")
        except ShortURL.DoesNotExist:
            print(f"Short code {short_code} not found")
            return Response(
                {"error": "Short code not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(f"Error during redirect: {e}")
            return Response(
                {"An unexpected error occurred. Please report this to our team."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return redirect(obj.original_url)
