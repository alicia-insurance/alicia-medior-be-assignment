from django.urls import reverse
from rest_framework.test import APITestCase
from django.utils import timezone
from .models import ShortURL


class ShortURLAPITests(APITestCase):

    def test_create_short_url(self):
        """Test creating a short URL with minimal data."""
        data = {'original_url': 'https://openai.com'}
        response = self.client.post(reverse('shorten-url'), data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('short_url', response.data)

    def test_custom_short_code(self):
        """Test creating a short URL with a custom code."""
        data = {
            'original_url': 'https://openai.com',
            'custom_short_code': 'OPENAI123'
        }
        response = self.client.post(reverse('shorten-url'), data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data['short_url'].endswith('/OPENAI123/'))

    def test_duplicate_custom_code(self):
        """Test that duplicate custom codes are not allowed."""
        ShortURL.objects.create(original_url='https://first.com', short_code='MYCODE')
        data = {
            'original_url': 'https://second.com',
            'custom_short_code': 'MYCODE'
        }
        response = self.client.post(reverse('shorten-url'), data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('custom_short_code', response.data)

    def test_expiry_validation_on_create(self):
        """Test that you cannot create a short URL with expiry in the past."""
        data = {
            'original_url': 'https://openai.com',
            'expires_at': (timezone.now() - timezone.timedelta(days=1)).isoformat()
        }
        response = self.client.post(reverse('shorten-url'), data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('expires_at', response.data)

    def test_expired_link_returns_410(self):
        """Test that expired links cannot be accessed."""
        expires_at = timezone.now() - timezone.timedelta(seconds=1)
        obj = ShortURL.objects.create(
            original_url='https://expired.com',
            short_code='EXPIRED',
            expires_at=expires_at
        )
        response = self.client.get(f'/short/{obj.short_code}/')
        self.assertEqual(response.status_code, 410)
        self.assertIn(b"expired", response.content)

    def test_redirect_works(self):
        """Test that the redirect endpoint sends you to the original URL."""
        obj = ShortURL.objects.create(
            original_url='https://openai.com',
            short_code='REDIRECTME'
        )
        response = self.client.get(f'/short/{obj.short_code}/', follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'https://openai.com')

    def test_stats_endpoint(self):
        """Test the stats API for a valid short code."""
        obj = ShortURL.objects.create(
            original_url='https://openai.com',
            short_code='STATS'
        )
        response = self.client.get(reverse('short-url-stats', args=[obj.short_code]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['short_code'], 'STATS')
        self.assertEqual(response.data['original_url'], 'https://openai.com')

    def test_invalid_short_code_redirect(self):
        """Test 404 is returned for a non-existent short code."""
        response = self.client.get('/short/DOESNOTEXIST/')
        self.assertEqual(response.status_code, 404)

    def test_list_requires_admin(self):
        """Test that listing all short URLs requires admin permissions."""
        # Not logged in as admin, should be forbidden or unauthorized
        response = self.client.get(reverse('short-url-list'))
        self.assertIn(response.status_code, [401, 403])  # Depends on auth config
