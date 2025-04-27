import logging
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, redirect
from url_shortener.models import ShortenUrl
from url_shortener.throttling import RedirectRateAnonThrottle, RedirectRateUserThrottle
from rest_framework.response import Response
from stats.redirect_counter import increment_redirect_count
from stats.task import save_request_counts

logger = logging.getLogger(__name__)

class RedirectToOriginalUrlView(APIView):

    throttle_classes = [RedirectRateAnonThrottle, RedirectRateUserThrottle]

    def get(self, request, short_code):

        url_obj = get_object_or_404(ShortenUrl, short_code=short_code)
        logger.debug("Short code %s -> %s",
                    short_code, url_obj.original_url)
        
        if url_obj.is_expired:
            logger.warning("Short code %s is expired", short_code)
            return Response({"error": "URL is expired"}, status=410)

        if url_obj.is_banned:
            logger.warning("Short code %s is banned", short_code)
            return Response({"error": "URL is banned"}, status=403)
        
        increment_redirect_count(url_obj.short_code)

        # The stats upadtes are made as a sepearate task
        # The stats are made to be kept in memory and flushed to the database
        # This is done to reduce the load on the database.
        # In current implementation, this operations is done for every request.
        # But if bellow fuction call is automated to be called at regular intervals,
        # using a task queue like Celery, it will be more efficient.
        save_request_counts()

        # Made the permanent redirect False, beauce then it is not possible
        # to band harmful URLs since the browser will cache the redirect.
        # Also the cacluations for the redirect will be not accurate.
        # Drawback: It will not be cached by the browser and will be fetched
        #           every time, increases the load on the server.
        return redirect(url_obj.original_url, permanent=False)