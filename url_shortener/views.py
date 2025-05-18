from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, redirect
from url_shortener.models import ShortURL
from url_shortener.serializers import ShortURLSerializer, ShortURLAccessCountSerializer
from url_shortener.utils import decode_code


class ShortenURLView(APIView):
    """
    Creates a shortened URL from an original URL via POST request.
    """

    def post(self, request):
        """Create a new short URL."""
        serializer = ShortURLSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        short_url = ShortURL.objects.create(
            original_url=serializer.validated_data["original_url"]
        )
        response_serializer = ShortURLSerializer(short_url)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class RedirectShortURLView(APIView):
    """
    Redirects a short URL code to its original URL.
    """

    def get(self, request, short_code):
        """Redirect to the original URL."""
        id = decode_code(short_code)
        url_obj = get_object_or_404(ShortURL, pk=id)
        url_obj.increment_access_count()
        return redirect(url_obj.original_url)


class ShortURLStatsView(APIView):
    """
    Retrieves access count statistics for a short URL.
    """

    def get(self, request, short_code):
        """Return access statistics for the short URL."""
        id = decode_code(short_code)
        url_obj = get_object_or_404(ShortURL, pk=id)
        serializer = ShortURLAccessCountSerializer(url_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
