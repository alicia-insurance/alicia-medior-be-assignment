from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.versioning import URLPathVersioning
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect
from url_shortener.models import ShortURL

class ShortenURLView(APIView):
    def post(self, request, *args, **kwargs):
        version = request.version
        data = request.data
        original_url = data.get("original_url", "http://alicia.insure")
        custom_alias = data.get("custom_alias", None)
        # TODO
        # need to validate the custom_alias if provided
        # create a unique short_alias if not provided
        # use API versioning
        # use serializers for better validation
        
        validator = URLValidator()
        try:
            validator(original_url)
        except ValidationError:
            return Response({"error": "Invalid URL"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "short_url": f"http://localhost:8000/short/{custom_alias}/"
        }, status=status.HTTP_201_CREATED)

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