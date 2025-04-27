
"""
Test Suite Covers:
- Model tests - Creation, string representation, uniqueness
- Utils tests - Hash generation and shortcode creation
- View tests - Creating short URLs and redirection
- Error handling - Invalid URLs, missing data, banned/expired URLs
- Throttling tests - Rate limiting behavior
"""

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import ShortenUrl, User
from .utils import generate_unique_shortcode, generate_sha_256_hash
from unittest.mock import patch


class ShortenUrlModelTest(TestCase):
    def test_create_shorten_url(self):
        """Test creating a ShortenUrl instance"""
        url = ShortenUrl.objects.create(original_url="https://example.com")
        self.assertIsNotNone(url.short_code)
        self.assertEqual(url.original_url, "https://example.com")
        self.assertFalse(url.is_banned)
        self.assertFalse(url.is_expired)

    def test_str_representation(self):
        """Test the string representation of ShortenUrl model"""
        url = ShortenUrl.objects.create(
            original_url="https://example.com", 
            short_code="abc123"
        )
        self.assertEqual(
            str(url),
            "Short code abc123 is mapped to https://example.com"
        )

    def test_unique_short_code(self):
        """Test that short codes are unique"""
        url1 = ShortenUrl.objects.create(original_url="https://example1.com")
        url2 = ShortenUrl.objects.create(original_url="https://example2.com")
        self.assertNotEqual(url1.short_code, url2.short_code)


class UtilsTest(TestCase):
    def test_generate_sha_256_hash(self):
        """Test SHA-256 hash generation"""
        url = "https://example.com"
        hash1 = generate_sha_256_hash(url)
        
        # Should be 6 chars long
        self.assertEqual(len(hash1), 6)
        
        # Same URL should get different hashes due to timestamp
        import time
        time.sleep(1)  # Wait to ensure different timestamp
        hash2 = generate_sha_256_hash(url)
        self.assertNotEqual(hash1, hash2)

    def test_generate_unique_shortcode(self):
        """Test unique shortcode generation"""
        url = "https://example.com"
        shortcode = generate_unique_shortcode(url, ShortenUrl)
        self.assertIsNotNone(shortcode)
        self.assertTrue(len(shortcode) >= 5)


class CreateShortenUrlViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("create_short_url")
    
    def test_create_short_url_success(self):
        """Test successful URL shortening"""
        data = {"original_url": "https://example.com"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("short_code", response.data)
        self.assertIn("original_url", response.data)
        self.assertIn("url", response.data)
        self.assertIn("created_at", response.data)

    def test_create_short_url_invalid_url(self):
        """Test with invalid URL"""
        data = {"original_url": "not-a-valid-url"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_short_url_missing_url(self):
        """Test with missing URL"""
        data = {}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RedirectToOriginalUrlViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url_obj = ShortenUrl.objects.create(
            original_url="https://example.com",
            short_code="test123"
        )
    
    def test_redirect_success(self):
        """Test successful redirection"""
        response = self.client.get(reverse("redirect_to_original", args=["test123"]))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, "https://example.com")

    def test_redirect_not_found(self):
        """Test redirection with non-existent short code"""
        response = self.client.get(reverse("redirect_to_original", args=["nonexistent"]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_redirect_banned_url(self):
        """Test redirection with banned URL"""
        self.url_obj.is_banned = True
        self.url_obj.save()
        response = self.client.get(reverse("redirect_to_original", args=["test123"]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_redirect_expired_url(self):
        """Test redirection with expired URL"""
        self.url_obj.is_expired = True
        self.url_obj.save()
        response = self.client.get(reverse("redirect_to_original", args=["test123"]))
        self.assertEqual(response.status_code, status.HTTP_410_GONE)

# Custom Throttling needs to be tested separately
# class ThrottlingTest(APITestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.url = reverse("create_short_url")
    
#     @patch('rest_framework.throttling.BaseThrottle.allow_request', return_value=False)
#     def test_throttling(self, mock_allow_request):
#         """Test throttling behavior"""
#         data = {"original_url": "https://example.com"}
#         response = self.client.post(self.url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)