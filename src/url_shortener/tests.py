from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import ShortenedURL


@override_settings(
    REST_FRAMEWORK={
        "DEFAULT_AUTHENTICATION_CLASSES": [],
        "DEFAULT_PERMISSION_CLASSES": [],
        "DEFAULT_THROTTLE_CLASSES": [],
        "DEFAULT_THROTTLE_RATES": {},
    }
)
class URLShortenerTests(TestCase):
    """
    Integration test suite for the URL Shortener API.

    Covers:
    - Creating short URLs with and without custom codes
    - Handling duplicate short codes
    - Redirection logic
    - Access statistics and increment logic
    """

    def setUp(self) -> None:
        """
        Setup test client and test data before each test.
        """
        self.client: APIClient = APIClient()
        user: User = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=user)

        self.base_url: str = "https://example.com"
        self.custom_code: str = "mycode123"

    def test_create_short_url(self) -> None:
        """
        Test creating a short URL from an original URL.
        """
        response = self.client.post(
            reverse("url_shortener:shorten_url"),
            data={"original_url": self.base_url},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("short_url", response.data)

    def test_create_short_url_with_custom_code(self) -> None:
        """
        Test creating a short URL using a custom short code.
        """
        response = self.client.post(
            reverse("url_shortener:shorten_url"),
            data={"original_url": self.base_url, "custom_code": self.custom_code},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(self.custom_code, response.data["short_url"])

    def test_duplicate_custom_code(self) -> None:
        """
        Test submitting a custom code that already exists in the DB.
        Should return 400 Bad Request.
        """
        ShortenedURL.objects.create(
            original_url=self.base_url, short_code=self.custom_code
        )
        response = self.client.post(
            reverse("url_shortener:shorten_url"),
            data={
                "original_url": "https://another-url.com",
                "custom_code": self.custom_code,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("custom_code", response.data)

    def test_redirect_view(self) -> None:
        """
        Test redirecting to the original URL using a valid short code.
        Should return 302 Found with correct location.
        """
        short_url = ShortenedURL.objects.create(
            original_url=self.base_url, short_code=self.custom_code
        )
        response = self.client.get(
            reverse("url_shortener:redirect_url", args=[short_url.short_code])
        )
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response["Location"], self.base_url)

    def test_redirect_not_found(self) -> None:
        """
        Test redirection with a non-existent short code.
        Should return 404 Not Found.
        """
        response = self.client.get(
            reverse("url_shortener:redirect_url", args=["noexist"])
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch("url_shortener.views.StatsView.throttle_classes", new=[])
    def test_stats_view(self) -> None:
        """
        Test retrieving statistics (access count and URL) for a valid short code.
        """
        short_url = ShortenedURL.objects.create(
            original_url=self.base_url, short_code=self.custom_code, access_count=3
        )
        response = self.client.get(
            reverse("url_shortener:url_stats", args=[short_url.short_code])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["access_count"], 3)
        self.assertEqual(response.data["original_url"], self.base_url)

    @patch("url_shortener.views.StatsView.throttle_classes", new=[])
    def test_stats_not_found(self) -> None:
        """
        Test retrieving stats for a non-existent short code.
        Should return 404 Not Found.
        """
        response = self.client.get(reverse("url_shortener:url_stats", args=["noexist"]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_existing_url_returns_same_code(self) -> None:
        """
        Test that shortening the same URL twice returns the same short code.
        """
        response1 = self.client.post(
            reverse("url_shortener:shorten_url"),
            data={"original_url": self.base_url},
            format="json",
        )
        response2 = self.client.post(
            reverse("url_shortener:shorten_url"),
            data={"original_url": self.base_url},
            format="json",
        )
        self.assertEqual(response1.data["short_url"], response2.data["short_url"])

    def test_access_count_increment_on_redirect(self) -> None:
        """
        Test that the access count increases with each redirect request.
        """
        short_url = ShortenedURL.objects.create(
            original_url=self.base_url, short_code=self.custom_code, access_count=0
        )
        for _ in range(3):
            self.client.get(
                reverse("url_shortener:redirect_url", args=[short_url.short_code])
            )
        short_url.refresh_from_db()
        self.assertEqual(short_url.access_count, 3)
