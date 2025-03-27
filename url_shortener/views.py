
from project import settings
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from django.core.cache import cache

from .models import URL, URLAccessLog
from .serializers import URLSerializer, URLAccessLogSerializer
from .utils import generate_short_code
from .validators import validate_url, validate_custom_code


class ShortenURL(APIView):
    def post(self, request):
        original_url = request.data.get("original_url")
        custom_code = request.data.get("custom_code")

        # Validate the original URL using your custom validate_url function
        try:
            validate_url(original_url)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Validate custom code if provided
        if custom_code:
            try:
                validate_custom_code(custom_code)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            # Check if custom code already exists in the database
            if URL.objects.filter(custom_code=custom_code).exists():
                return Response({"error": "Custom short code already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Generate short code if not provided
        short_code = custom_code or generate_short_code()

        try:
            # Try to create or retrieve the URL object
            url, created = URL.objects.get_or_create(original_url=original_url, short_code=short_code, custom_code=custom_code  )
        except IntegrityError:
            # Handle the IntegrityError if the short_code already exists
            return Response({"error": f"Short code '{short_code}' already exists. Please choose a different one."},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({"short_url": f"{settings.BASE_URL}/short/{url.short_code}"}, status=status.HTTP_201_CREATED)


class RedirectURL(APIView):
    def get(self, request, short_code):
        cached_url = cache.get(short_code)

        if cached_url:
            return redirect(cached_url)

        try:
            url = URL.objects.get(short_code=short_code)
            url.visit_count += 1
            url.last_accessed = now()
            url.save()

            # Cache the URL for faster access next time
            cache.set(short_code, url.original_url, timeout=3600)  # Cache for 1 hour

            # Log the access
            URLAccessLog.objects.create(
                url=url,
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT')
            )

            return redirect(url.original_url)
        except URL.DoesNotExist:
            return Response({"error": "URL not found."}, status=status.HTTP_404_NOT_FOUND)


class URLStats(APIView):
    def get(self, request, short_code):
        try:
            url = URL.objects.get(short_code=short_code)
            logs = URLAccessLog.objects.filter(url=url)
            log_serializer = URLAccessLogSerializer(logs, many=True)
            url_serializer = URLSerializer(url)
            return Response({
                "url_details": url_serializer.data,
                "access_logs": log_serializer.data
            })
        except URL.DoesNotExist:
            return Response({"error": "URL not found."}, status=status.HTTP_404_NOT_FOUND)
