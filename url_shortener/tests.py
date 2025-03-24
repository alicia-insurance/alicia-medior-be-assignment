from rest_framework.test import APIClient
from django.core.cache import cache
from rest_framework import status
from django.test import TestCase
from django.urls import reverse

from .models import ShortURL

class URLShortenerTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_url = "https://example.com/page"
        self.shorten_url = reverse('shorten-url')

    def test_shorten_url_with_random_code(self):
        response = self.client.post(self.shorten_url, {"original_url": self.valid_url}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("short_url", response.data)
        self.assertEqual(response.data["original_url"], self.valid_url)

    def test_shorten_url_with_custom_code(self):
        response = self.client.post(self.shorten_url, {"original_url": self.valid_url, "short_code": "custom1"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["short_code"], "custom1")

    def test_shorten_url_custom_code_conflict(self):
        ShortURL.objects.create(original_url=self.valid_url, short_code="conflict")
        response = self.client.post(self.shorten_url, {"original_url": self.valid_url, "short_code": "conflict"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("short_code", response.data)

    def test_redirect_view_with_cache(self):
        short_url_obj = ShortURL.objects.create(original_url=self.valid_url)
        cache_key = f"short_code:{short_url_obj.short_code}"
        cache.set(cache_key, self.valid_url, timeout=3600)
        redirect_url = reverse('redirect-url', args=[short_url_obj.short_code])
        response = self.client.get(redirect_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.valid_url)

    def test_stats_view(self):
        short_url_obj = ShortURL.objects.create(original_url=self.valid_url, visit_count=5)
        stats_url = reverse('url-stats', args=[short_url_obj.short_code])
        response = self.client.get(stats_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['visit_count'], 5)
        self.assertEqual(response.data['original_url'], self.valid_url)


class URLShortenerRateLimitTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_url = "https://example.com/page"
        self.shorten_url = reverse('shorten-url')

    def test_rate_limiting(self):
        for _ in range(10):
            response = self.client.post(self.shorten_url, {"original_url": self.valid_url}, format='json')
            self.assertNotEqual(response.status_code, 429)  # Should succeed within limit

        # 11th request should be rate-limited
        response = self.client.post(self.shorten_url, {"original_url": self.valid_url}, format='json')
        self.assertEqual(response.status_code, 429)
