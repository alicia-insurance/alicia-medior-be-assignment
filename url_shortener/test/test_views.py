from django.conf import settings
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from url_shortener.models import ShortURL

TEST_API_KEY = "test_api_key"


@override_settings(API_KEY=TEST_API_KEY)
class ShortenURLAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.auth = {"HTTP_X_API_KEY": TEST_API_KEY}

    def test_shorten_url_success(self):
        url = reverse("shorten-url", kwargs={"version": "v1"})
        data = {"original_url": "http://alicia.insure"}
        response = self.client.post(url, data, format="json", **self.auth)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("short_url", response.data)

    def test_shorten_url_invalid(self):
        url = reverse("shorten-url", kwargs={"version": "v1"})
        data = {"original_url": "not-a-url"}
        response = self.client.post(url, data, format="json", **self.auth)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_custom_alias(self):
        url = reverse("shorten-url", kwargs={"version": "v1"})
        data = {"original_url": "http://alicia.insure", "custom_alias": "myalias"}
        response = self.client.post(url, data, format="json", **self.auth)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("myalias", response.data["short_url"])


class RedirectShortURLTest(TestCase):
    def setUp(self):
        self.obj = ShortURL.objects.create(
            original_url="http://alicia.insure", short_alias="redir", is_active=True
        )
        self.client = APIClient()

    def test_redirect(self):
        url = reverse("redirect-short-url", args=["redir"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "http://alicia.insure")

    def test_redirect_inactive(self):
        self.obj.is_active = False
        self.obj.save()
        url = reverse("redirect-short-url", args=["redir"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


@override_settings(API_KEY=TEST_API_KEY)
class ShortURLStatsTest(TestCase):
    def setUp(self):
        self.obj = ShortURL.objects.create(
            original_url="http://alicia.insure", short_alias="redir", is_active=True
        )
        self.client = APIClient()
        self.auth = {"HTTP_X_API_KEY": TEST_API_KEY}

    def test_stats(self):
        url = reverse(
            "short-url-stats", kwargs={"version": "v1", "short_code": "redir"}
        )
        response = self.client.get(url, **self.auth)
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_count", response.data)
        self.assertIn("created_at", response.data)
