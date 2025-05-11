from rest_framework import generics
from django.http import HttpResponseRedirect
from .serializers import URLShortenerSerializer, ShortenedURLStatsSerializer
from .models import ShortenedURL, ShortenURLAccessLog


class URLShortenView(generics.CreateAPIView):
    """
    API Endpoint for shorten given URL
    """

    queryset = ShortenedURL.objects.all()
    serializer_class = URLShortenerSerializer


class OriginalURLView(generics.RetrieveAPIView):
    """
    API Endpoint to redirect the shortened URL to original URL
    """

    queryset = ShortenedURL.objects.all()
    serializer_class = URLShortenerSerializer

    lookup_field = "short_url_key"

    def retrieve(self, request, *args, **kwargs):
        url_object = self.get_object()

        ShortenURLAccessLog.objects.create(short_url_key=url_object)
        return HttpResponseRedirect(url_object.original_url)


class URLStatsView(generics.RetrieveAPIView):
    """
    API endpoint to list the shortened URL stats
    """

    queryset = ShortenedURL.objects.all()
    serializer_class = ShortenedURLStatsSerializer
    lookup_field = "short_url_key"
