"""
API views for URL Shortener.

Uses APIView for full control; scalable to generic/list views.
OpenAPI (Swagger) examples provided for all main endpoints.
"""
from django.db.models import F
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status, throttling, permissions
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseGone
from .models import ShortURL
from .serializers import ShortenURLResponseSerializer, ShortenURLSerializer, ShortURLStatsSerializer
from .pagination import CustomShortURLPagination
from drf_spectacular.utils import extend_schema, OpenApiExample


class BurstRateThrottle(throttling.UserRateThrottle):
    rate = '10/min'


class ShortenURLAPIView(APIView):
    """
    POST /api/shorten/

    Shortens a given long URL with option for expiry and custom code.
    """
    throttle_classes = [BurstRateThrottle]
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Shorten a long URL",
        description=(
            "Creates a short URL from the provided original URL. "
            "Optionally allows a custom code and expiry."
        ),
        request=ShortenURLSerializer,
        responses={201: ShortenURLResponseSerializer},
        examples=[
            OpenApiExample(
                'Basic Example',
                value={"original_url": "https://openai.com"},
                request_only=True,
            ),
            OpenApiExample(
                'Response Example',
                value={"short_url": "http://127.0.0.1:8000/short/xXL2ZB/"},
                response_only=True,
                status_codes=["201"],
            ),
        ],
        tags=["Shortener"]
    )
    def post(self, request):
        serializer = ShortenURLSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            short_url = request.build_absolute_uri(f'/short/{obj.short_code}/')
            return Response({"short_url": short_url}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RedirectShortURLView(APIView):
    """
    GET /short/<short_code>/

    Redirects to the original URL, tracks stats, blocks expired links.
    """
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        summary="Redirect to the original URL",
        description=(
            "Redirects users to the original long URL using the short code."
            " Returns 410 if expired or 404 if not found."),
        responses={
            302: None,  # Swagger will document this as a redirect
            404: None,
            410: None,
        },
        tags=["Shortener"]
    )
    def get(self, request, short_code):
        url_obj = get_object_or_404(ShortURL, short_code=short_code)
        if url_obj.is_expired():
            return HttpResponseGone("This short link has expired.")
        # Atomic increment for thread safety
        ShortURL.objects.filter(pk=url_obj.pk).update(access_count=F('access_count') + 1)
        # Optionally: url_obj.refresh_from_db(fields=["access_count"])
        return redirect(url_obj.original_url)


class ShortURLStatsAPIView(APIView):
    """
    GET /api/stats/<short_code>/

    Returns access and metadata stats for the short URL.
    """
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Get stats for a short URL",
        responses={200: ShortURLStatsSerializer},
        tags=["Shortener"]
    )
    def get(self, request, short_code):
        url_obj = get_object_or_404(ShortURL, short_code=short_code)
        serializer = ShortURLStatsSerializer(url_obj)
        return Response(serializer.data)


@extend_schema(
    summary="List all Short URLs",
    description="Returns a paginated list of all Short URLs (admin only).",
    tags=["Shortener"]
)
class ShortURLListView(ListAPIView):
    """
    GET /api/shorturls/

    Paginated, ordered list of all ShortURLs (admin/future multi-tenant ready).
    """
    queryset = ShortURL.objects.all()
    serializer_class = ShortURLStatsSerializer
    pagination_class = CustomShortURLPagination
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return super().get_queryset()
