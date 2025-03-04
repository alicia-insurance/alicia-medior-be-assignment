import random
import string

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ShortenedURL
from .serializers import ShortenedURLSerializer


def generate_short_code(length=6):
    """
    Generates a random short code consisting of alphanumeric characters.

    Args:
        length (int): The length of the generated short code. Defaults to 6.

    Returns:
        str: The generated short code.
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_unique_short_code(custom_alias=None):
    """
    Generates a unique short code. If a custom alias is provided, it checks if it is
    available; otherwise, it generates a random short code.

    Args:
        custom_alias (str, optional): The custom alias provided by the user.
        Defaults to None.

    Returns:
        str: The unique short code (either the custom alias or a newly generated one).

    Raises:
        ValueError: If the custom alias is already taken in the database.
    """
    # Check if the user has provided a custom alias
    if custom_alias:
        # Check if the custom alias is already used in the database
        if ShortenedURL.objects.filter(short_code=custom_alias).exists():
            raise ValueError(
                "This custom alias is already taken. Please choose another one."
            )
        return custom_alias

    # Generate a random short code if no custom alias is provided
    short_code = generate_short_code()

    # Ensure the short code is unique
    while ShortenedURL.objects.filter(short_code=short_code).exists():
        short_code = generate_short_code()

    return short_code


# API view to shorten a URL
@api_view(['POST'])
def shorten_url(request):
    """
    API view to shorten a given original URL. Optionally, custom alias can be provided.
    If a custom alias is not provided, a random one is generated. If the original URL
    already exists, the existing shortened URL is returned.

    Args:
        request (Request): The HTTP request containing the original URL and optionally
        a custom alias.

    Returns:
        Response: A response containing the shortened URL or an error message.
    """
    original_url = request.data.get('original_url')
    custom_alias = request.data.get(
        'custom_alias', None
    )  # Get the custom alias if provided

    if not original_url:
        return Response(
            {"error": "original_url field is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not custom_alias:
        # Now check if the original URL already exists in the database
        existing_mapping = ShortenedURL.objects.filter(
            original_url=original_url
        ).first()

        if existing_mapping:
            # Return the existing short URL if the URL already exists in the database
            return Response(
                ShortenedURLSerializer(existing_mapping).data, status=status.HTTP_200_OK
            )

    try:
        short_code = generate_unique_short_code(custom_alias)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # Save the URL mapping in the database
    shortened_url = ShortenedURL(
        original_url=original_url, short_code=short_code, custom_alias=custom_alias
    )
    shortened_url.save()

    # Return the short URL in the response
    return Response(
        ShortenedURLSerializer(shortened_url).data, status=status.HTTP_201_CREATED
    )


# API view to redirect to the original URL using the short code
@api_view(['GET'])
def redirect_url(request, short_code):
    """
    API view to redirect the user to the original URL using the provided short code.
    The access count is also incremented each time the URL is accessed.

    Args:
        request (Request): The HTTP request containing the short code.
        short_code (str): The shortened URL's code.

    Returns:
        HttpResponseRedirect: Redirects the user to the original URL.
    """
    shortened_url = get_object_or_404(ShortenedURL, short_code=short_code)

    # Update the access count (if stats are tracked)
    shortened_url.access_count += 1
    shortened_url.save()

    # Redirect to the original URL
    return HttpResponseRedirect(shortened_url.original_url)


@api_view(['GET'])
def get_url_stats(request, short_code):
    """
    API view to get the statistics for a shortened URL, including the access count.

    Args:
        request (Request): The HTTP request containing the short code.
        short_code (str): The shortened URL's code.

    Returns:
        Response: A response containing the statistics (short code, original URL, access count). # noqa
    """
    shortened_url = get_object_or_404(ShortenedURL, short_code=short_code)

    # Return stats as JSON
    stats = {
        'short_code': shortened_url.short_code,
        'original_url': shortened_url.original_url,
        'access_count': shortened_url.access_count,
    }

    return Response(stats)
