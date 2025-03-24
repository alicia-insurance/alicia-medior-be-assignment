
from django.shortcuts import get_object_or_404, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache
from rest_framework import status
from django.views import View
from django.db import models

from .serializers import ShortURLSerializer
from .models import ShortURL

class ShortenURLView(APIView):

    def post(self, request):
        serializer = ShortURLSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            short_url_instance = serializer.save()
            response_serializer = ShortURLSerializer(short_url_instance, context={'request': request})
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RedirectView(View):

    def get(self, request, short_code):
        cache_key = f"short_code:{short_code}"
        original_url = cache.get(cache_key)

        if original_url is None:
            url_obj = get_object_or_404(ShortURL, short_code=short_code)
            original_url = url_obj.original_url
            cache.set(cache_key, original_url, timeout=3600)
        else:
            url_obj = ShortURL.objects.only("id", "visit_count").get(short_code=short_code)

        ShortURL.objects.filter(id=url_obj.id).update(visit_count=models.F("visit_count") + 1)

        return redirect(original_url)


class StatsView(APIView):

    def get(self, request, short_code):
        try:
            url_obj = ShortURL.objects.get(short_code=short_code)
        except ShortURL.DoesNotExist:
            return Response({"error": "Short URL not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ShortURLSerializer(url_obj, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
