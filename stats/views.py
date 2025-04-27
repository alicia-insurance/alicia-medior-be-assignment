import logging

from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from url_shortener.models import ShortenUrl
from .models import RedirectCount
from rest_framework.response import Response



class RedirectCountView(APIView):

    def get(self, request, short_code):

        url_obj = get_object_or_404(ShortenUrl, short_code=short_code)
        stat_obj = get_object_or_404(RedirectCount, shorten_url=url_obj)
        _output = {
            "short_code": url_obj.short_code,
            "original_url": url_obj.original_url,
            "created_at": url_obj.created_at,
            "is_expired": url_obj.is_expired,
            "is_banned": url_obj.is_banned,
            "access_count": stat_obj.redirect_count,
        }
        return Response(_output, status=200)