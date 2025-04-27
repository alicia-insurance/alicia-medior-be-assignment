import logging
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from url_shortener.serializers.shorten_url import CreateShortenUrlPublicSerializer
from url_shortener.throttling import CreateShortUrlRateAnonThrottle
from url_shortener.throttling import CreateShortUrlRateUserThrottle

logger = logging.getLogger(__name__)


class CreateShortenUrlView(APIView):

    throttle_classes = [CreateShortUrlRateAnonThrottle, CreateShortUrlRateUserThrottle]

    def post(self, request):
        logger.info("Shorten URL Request: %s", request.data)

        serializer = CreateShortenUrlPublicSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            logger.warning("Invalid shortening request: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        url_instance = serializer.save()
        logger.info("Successfully created short URL: %s -> %s",
                    url_instance.original_url, serializer.data.get('url'))
        return Response(serializer.data, status=status.HTTP_201_CREATED)

        

