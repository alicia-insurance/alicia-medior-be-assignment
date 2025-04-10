from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import ShortenedURL
from .serializers import ShortenedURLSerializer

@swagger_auto_schema(
    method='post',
    request_body=ShortenedURLSerializer,
    responses={
        201: openapi.Response('Created', ShortenedURLSerializer),
        400: 'Bad Request'
    },
    operation_description="Create a short URL from a long URL",
    operation_summary="Shorten a URL",
    security=[]
)
@api_view(['POST'])
def shorten_url(request):
    """
    Create a short URL
    
    Accepts a long URL and returns a shortened version.
    Example:
    {
        "original_url": "https://example.com/very/long/url"
    }
    """
    serializer = ShortenedURLSerializer(data=request.data)
    if serializer.is_valid():
        shortened_url = serializer.save()
        return Response({
            'short_code': shortened_url.short_code,
            'short_url': f"{request.build_absolute_uri('/')}short/{shortened_url.short_code}/",
            'original_url': shortened_url.original_url,
            'created_at': shortened_url.created_at
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'short_code',
            openapi.IN_PATH,
            description="The short code for the URL",
            type=openapi.TYPE_STRING
        )
    ],
    responses={
        302: 'Redirects to original URL',
        404: 'Not Found'
    },
    operation_description="Redirect to original URL using short code",
    operation_summary="Redirect to original URL",
    security=[]
)
@api_view(['GET'])
def redirect_to_original(request, short_code):
    """
    Redirect to original URL
    
    When accessed, this endpoint will redirect to the original long URL
    associated with the provided short code.
    """
    shortened_url = get_object_or_404(ShortenedURL, short_code=short_code)
    shortened_url.access_count += 1
    shortened_url.save()
    return HttpResponseRedirect(shortened_url.original_url)

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'short_code',
            openapi.IN_PATH,
            description="The short code for the URL",
            type=openapi.TYPE_STRING
        )
    ],
    responses={
        200: openapi.Response('OK', ShortenedURLSerializer),
        404: 'Not Found'
    },
    operation_description="Get statistics for a short URL",
    operation_summary="Get URL statistics",
    security=[]
)
@api_view(['GET'])
def url_stats(request, short_code):
    """
    Get URL statistics
    
    Returns access count and other statistics for a given short URL.
    """
    shortened_url = get_object_or_404(ShortenedURL, short_code=short_code)
    serializer = ShortenedURLSerializer(shortened_url)
    return Response(serializer.data)