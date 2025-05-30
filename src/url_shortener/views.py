"""
URL Shortener API Views

Provides API endpoints to:
- Create shortened URLs
- Redirect short codes to original URLs
- View statistics on shortened URLs
"""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ShortenedURL
from .serializers import ShortenedURLResponseSerializer, ShortenURLSerializer


class ShortenURLView(APIView):
    """
    Handles POST requests to shorten a given URL.

    Accepts an original URL (and optionally a custom short code),
    and returns a shortened version of the URL.
    """

    @swagger_auto_schema(
        operation_summary="Create or retrieve a shortened URL",
        operation_description=(
            "Accepts a JSON payload with an original URL and optionally a custom short code.\n\n"
            "- If a custom code is provided, it must be unique.\n"
            "- If the original URL was previously shortened, the existing short code is reused."
        ),
        request_body=ShortenURLSerializer,
        responses={
            201: openapi.Response(
                description="Short URL created",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "short_url": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="The generated shortened URL",
                        )
                    },
                ),
            ),
            400: "Bad Request – invalid input or duplicate short code",
        },
    )
    def post(self, request: HttpRequest) -> Response:
        """
        Create or retrieve a shortened URL for the given original URL.

        Args:
            request (HttpRequest): The HTTP POST request with JSON data.

        Returns:
            Response: A JSON response containing the shortened URL or error details.
        """
        serializer = ShortenURLSerializer(data=request.data)
        if serializer.is_valid():
            original_url: str = serializer.validated_data["original_url"]
            custom_code: str | None = serializer.validated_data.get("custom_code")

            if custom_code:
                obj = ShortenedURL.objects.create(
                    original_url=original_url,
                    short_code=custom_code,
                )
            else:
                obj, _ = ShortenedURL.objects.get_or_create(original_url=original_url)

            short_url = f"http://localhost/short/{obj.short_code}/"
            return Response({"short_url": short_url}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(cache_page(60 * 2), name="get")  # Cache redirects for 2 minutes
class RedirectView(APIView):
    """
    Redirects a short code to its original URL.

    Also increments the access count each time it's used.
    """

    @swagger_auto_schema(
        operation_summary="Redirect to original URL",
        operation_description=(
            "Given a short code, this endpoint redirects to the original URL.\n"
            "It also increments the access count for tracking purposes."
        ),
        responses={
            302: "Found – Redirect to original URL",
            404: "Not Found – Invalid or expired short code",
        },
    )
    def get(self, request: HttpRequest, short_code: str) -> HttpResponse:
        """
        Redirects the user to the original URL based on the short code.

        Args:
            request (HttpRequest): The HTTP GET request.
            short_code (str): The unique short code of the shortened URL.

        Returns:
            HttpResponse: Redirect to the original URL.
        """
        url_instance: ShortenedURL = get_object_or_404(
            ShortenedURL, short_code=short_code
        )
        url_instance.access_count += 1
        url_instance.save()
        return redirect(url_instance.original_url)


@method_decorator(cache_page(60 * 5), name="get")  # Cache for 5 minutes
@method_decorator(vary_on_headers("Authorization"), name="get")
class StatsView(RetrieveAPIView):
    """
    Returns statistics for a given shortened URL, such as access count and original URL.
    """

    queryset = ShortenedURL.objects.all()
    serializer_class = ShortenedURLResponseSerializer
    lookup_field = "short_code"

    @swagger_auto_schema(
        operation_summary="Retrieve statistics for a short URL",
        operation_description=(
            "Returns metadata and usage stats for a given short code, "
            "including the original URL, access count, and creation timestamp."
        ),
        responses={
            200: ShortenedURLResponseSerializer,
            404: "Not Found – Invalid short code",
        },
    )
    def get(self, request: HttpRequest, *args, **kwargs) -> Response:
        """
        Retrieve statistics for a given short code.

        Args:
            request (HttpRequest): The HTTP GET request.
            *args: Additional arguments.
            **kwargs: Expected to include 'short_code'.

        Returns:
            Response: JSON containing access stats and original URL.
        """
        return super().get(request, *args, **kwargs)
