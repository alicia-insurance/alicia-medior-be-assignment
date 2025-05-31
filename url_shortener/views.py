from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, redirect
from .models import ShortURL
from .serializers import ShortURLSerializer
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit

class ShortenURLView(APIView):
    @method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=False))
    def post(self, request):
        if getattr(request, 'limited', False):
            return Response({"detail": "Rate limit exceeded. Max 5 requests per minute."}, status=429)

        serializer = ShortURLSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RedirectURLView(APIView):
    def get(self, short_code):
        url_entry = get_object_or_404(ShortURL, short_code=short_code)
        url_entry.access_count += 1
        url_entry.save()
        return redirect(url_entry.original_url)

class URLStatsView(APIView):
    def get(self, short_code):
        url_entry = get_object_or_404(ShortURL, short_code=short_code)
        return Response({
            "original_url": url_entry.original_url,
            "short_code": url_entry.short_code,
            "access_count": url_entry.access_count,
            "created_at": url_entry.created_at
        })
