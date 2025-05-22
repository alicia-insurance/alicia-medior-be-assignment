from django.utils import timezone
from django.shortcuts import redirect, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ShortURL
from .serializers import ShortURLSerializer, URLStatsSerializer
from .utils.validators import generate_unique_alias
from .constants.messages import ERROR_MESSAGES
from url_shortener.utils.throttling import ShortURLCreateThrottle, RedirectThrottle, URLStatsThrottle
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.exceptions import ValidationError

class URLShortenerView(APIView):

    throttle_classes = [ShortURLCreateThrottle]

    @swagger_auto_schema(
        operation_description="Create a shortened URL",
        request_body=ShortURLSerializer,
        responses={
            201: ShortURLSerializer,
            400: "Bad Request"
        }
    )

    def post(self, request):
        serializer = ShortURLSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            error_messages = []
            for field, messages in e.detail.items():
                error_messages.extend(messages)
            return Response(
                {"error": " ".join(str(msg) for msg in error_messages)},
                status=status.HTTP_400_BAD_REQUEST
            )

        original_url = serializer.validated_data['original_url']
        custom_alias = request.data.get('custom_alias', None)

        existing_url = ShortURL.objects.filter(original_url=original_url).first()

        if existing_url:
            return Response(
                {"error": ERROR_MESSAGES['URL_ALREADY_EXISTS_ERROR']},
                status=status.HTTP_400_BAD_REQUEST
            )

        # If custom alias is provided, check if it's already taken
        if custom_alias:
            if ShortURL.objects.filter(short_alias=custom_alias).exists():
                return Response(
                    {"error": ERROR_MESSAGES['CUS_URL_ALREADY_EXISTS_ERROR']},
                    status=status.HTTP_400_BAD_REQUEST
                )
            short_alias = custom_alias
            is_custom_url = True
        else:
            short_alias = generate_unique_alias()
            is_custom_url = False

        short_url = ShortURL.objects.create(
            original_url= serializer.validated_data['original_url'],
            short_alias= short_alias,
            is_custom_url=is_custom_url
        )
        return Response(
            ShortURLSerializer(short_url).data,
            status=status.HTTP_201_CREATED
        )

class URLStatsView(APIView):
    """Handle URL statistics operations"""
    throttle_classes = [URLStatsThrottle]

    @swagger_auto_schema(
        operation_description="Get URL statistics",
        responses={
            200: URLStatsSerializer,
            404: "URL not found"
        }
    )

    def get(self, request, short_code):
        try:
            short_url_obj = get_object_or_404(ShortURL, short_alias=short_code)
            if not short_url_obj.is_active:
                return Response(
                    {"error": ERROR_MESSAGES['URL_INACTIVE']},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = URLStatsSerializer(short_url_obj)
            return Response(serializer.data)
        except Exception:
            return Response(
                {"error": ERROR_MESSAGES['UNEXPECTED_ERROR']},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class URLRedirectView(APIView):
    """Handle URL redirection operations"""
    throttle_classes = [RedirectThrottle]

    @swagger_auto_schema(
        operation_description="Redirect to original URL",
        responses={
            302: "Redirect to original URL",
            404: "URL not found"
        }
    )

    def get(self, request, short_code):
        try:
            short_url_obj = get_object_or_404(ShortURL, short_alias=short_code)
            if not short_url_obj.is_active:
                return Response(
                    {"error": ERROR_MESSAGES['URL_INACTIVE']},
                    status=status.HTTP_404_NOT_FOUND
                )

            self._update_url_stats(short_url_obj)
            return redirect(short_url_obj.original_url)

        except Exception:
            return Response(
                {"error": ERROR_MESSAGES['UNEXPECTED_ERROR']},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _update_url_stats(self, url_obj):
        """Update URL statistics"""
        url_obj.access_count += 1
        url_obj.last_accessed = timezone.now()
        url_obj.save()