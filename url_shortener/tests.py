import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
django.setup()

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from project import settings
from .models import URL
from .utils import generate_short_code


class URLShortenerTest(TestCase):
    """Test cases for shortening URLs, redirection, and rate limiting."""

    def setUp(self):
        """Set up test data for the tests."""
        self.valid_url = "https://www.google.com"
        self.invalid_url = "not_a_valid_url"
        self.short_code = generate_short_code()
        self.custom_code = "mycustomcode"

        # Create a URL entry for testing
        self.url_data = {
            "original_url": self.valid_url,
            "short_code": self.short_code
        }
        self.custom_url_data = {
            "original_url": self.valid_url,
            "custom_code": self.custom_code
        }

    def test_shorten_url_success(self):
        """Test that shortening a valid URL returns a valid short URL."""
        response = self.client.post(reverse('shorten_url'), self.url_data, format='json',
                                    content_type='application/json')

        # Check that the response status code is 201 (created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the response contains the short_url
        self.assertIn('short_url', response.data)

    def test_shorten_url_with_custom_code(self):
        """Test that shortening a URL with a custom code works."""
        response = self.client.post(reverse('shorten_url'), self.custom_url_data, format='json',
                                    content_type='application/json')

        # Check that the response status code is 201 (created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the short_url is correctly formed using BASE_URL and custom code
        expected_short_url = f"{settings.BASE_URL}/short/{self.custom_code}"
        self.assertEqual(response.data['short_url'], expected_short_url)

    def test_shorten_url_with_invalid_url(self):
        """Test that providing an invalid URL returns a 400 error."""
        invalid_data = {"original_url": self.invalid_url}
        response = self.client.post(reverse('shorten_url'), invalid_data, format='json',
                                    content_type='application/json')

        # Check that the response status code is 400 (bad request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_shorten_url_with_invalid_custom_code(self):
        """Test that providing an invalid custom code returns a 400 error."""
        invalid_custom_code = "inv@lidcode!"  # Example of an invalid custom code
        invalid_custom_data = {
            "original_url": self.valid_url,
            "custom_code": invalid_custom_code
        }
        response = self.client.post(reverse('shorten_url'), invalid_custom_data, format='json',
                                    content_type='application/json')

        # Check that the response status code is 400 (bad request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Custom short codes can only contain letters, digits, dashes, and underscores.", response.data['error'])

    def test_redirect_url_success(self):
        """Test that the short URL redirects to the original URL."""
        # First, create a URL entry
        url = URL.objects.create(original_url=self.valid_url, short_code=self.short_code)

        # Perform a GET request to the short URL (using the short code)
        response = self.client.get(reverse('redirect_url', kwargs={'short_code': self.short_code}))

        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        # Check that the redirect location is the original URL
        self.assertEqual(response['Location'], self.valid_url)

    def test_redirect_url_not_found(self):
        """Test that trying to redirect to a non-existent short URL returns a 404 error."""
        non_existent_code = "nonexistentcode"
        response = self.client.get(reverse('redirect_url', kwargs={'short_code': non_existent_code}))

        # Check that the response status code is 404 (not found)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_url_stats_success(self):
        """Test that stats for a shortened URL are returned."""
        # First, create a URL entry and access it
        url = URL.objects.create(original_url=self.valid_url, short_code=self.short_code)
        response = self.client.get(reverse('url_stats', kwargs={'short_code': self.short_code}))

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response contains URL stats
        self.assertIn('url_details', response.data)
        self.assertEqual(response.data['url_details']['original_url'], self.valid_url)
        self.assertIn('access_logs', response.data)  # Should be empty initially

    def test_url_stats_not_found(self):
        """Test that stats for a non-existent short URL return a 404 error."""
        non_existent_code = "nonexistentcode"
        response = self.client.get(reverse('url_stats', kwargs={'short_code': non_existent_code}))

        # Check that the response status code is 404 (not found)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_custom_code_collision(self):
        """Test that a custom code collision raises an error."""
        # First, create a URL entry with a custom code
        URL.objects.create(original_url=self.valid_url, custom_code=self.custom_code)

        # Try to create another URL with the same custom code
        response = self.client.post(reverse('shorten_url'), self.custom_url_data, format='json',
                                    content_type='application/json')

        # Check that the response status code is 400 (bad request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Custom short code already exists.", response.data['error'])


class URLModelTest(TestCase):
    """Test cases for URL model behaviors."""

    def test_short_code_creation(self):
        """Test that a URL can be created with a custom short code."""
        url = URL.objects.create(original_url="https://www.test.com", short_code="abc123")
        self.assertEqual(url.short_code, "abc123")

    def test_custom_code_creation(self):
        """Test that a URL can be created with a custom code."""
        url = URL.objects.create(original_url="https://www.test.com", custom_code="my-custom")
        self.assertEqual(url.custom_code, "my-custom")

    def test_redirection(self):
        """Test that accessing a short URL redirects to the original URL."""
        url = URL.objects.create(original_url="https://www.test.com", short_code="xyz789")
        response = self.client.get(f'/short/xyz789/')
        self.assertEqual(response.status_code, 302)  # 302 means redirection
