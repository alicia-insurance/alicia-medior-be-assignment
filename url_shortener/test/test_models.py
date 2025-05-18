from django.test import TestCase

from url_shortener.models import ShortURL

class ShortURLModelTest(TestCase):
    def test_create_shorturl(self):
        obj = ShortURL.objects.create(
            original_url="https://alicia.insure",
            short_alias="alicia"
        )
        self.assertEqual(obj.access_count, 0)
        self.assertTrue(obj.is_active)
        self.assertEqual(str(obj), "alicia -> https://alicia.insure")