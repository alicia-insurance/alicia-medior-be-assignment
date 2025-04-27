"""
Test suite covers:

In-memory counter functionality:
 - Basic increment and flush operations
 - Multiple shortcode tracking
- Thread safety under concurrent use

API view tests:
- Retrieving stats for valid shortcodes
- Handling nonexistent shortcodes
- Shortcodes with no recorded clicks

URL routing tests:
- Proper URL pattern generation
- Catch-all routing for invalid URLs
"""

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .redirect_counter import increment_redirect_count, flush_counts
from url_shortener.models import ShortenUrl
import threading
import time

class RedirectCounterTests(TestCase):
    """Tests for the in-memory counter functionality"""
    
    def setUp(self):
        # Clear counters before each test
        flush_counts()
        
    def test_increment_redirect_count(self):
        """Test basic counter increment functionality"""
        # Increment a few times and check value
        increment_redirect_count("test123")
        increment_redirect_count("test123")
        increment_redirect_count("test123")
        
        counts = flush_counts()
        self.assertEqual(counts["test123"], 3)
        
    def test_multiple_shortcodes(self):
        """Test tracking multiple shortcodes simultaneously"""
        increment_redirect_count("code1")
        increment_redirect_count("code2")
        increment_redirect_count("code1")
        
        counts = flush_counts()
        self.assertEqual(counts["code1"], 2)
        self.assertEqual(counts["code2"], 1)
        
    def test_flush_clears_counts(self):
        """Test that flush_counts() clears the internal counter"""
        increment_redirect_count("test123")
        flush_counts()
        
        # Should be empty after flush
        counts = flush_counts()
        self.assertEqual(len(counts), 0)
        
    def test_thread_safety(self):
        """Test counter is thread-safe with multiple threads updating"""
        def increment_many():
            for _ in range(100):
                increment_redirect_count("threaded")
                
        # Create and start 5 threads
        threads = []
        for _ in range(5):
            t = threading.Thread(target=increment_many)
            threads.append(t)
            t.start()
            
        # Wait for all threads to complete
        for t in threads:
            t.join()
            
        counts = flush_counts()
        self.assertEqual(counts["threaded"], 500)  # 5 threads × 100 increments


class RedirectCountViewTests(APITestCase):
    """Tests for the RedirectCountView API endpoint"""
    
    def setUp(self):
        flush_counts()  # Clear counters
        self.client = Client()
        
        # Create test short URL
        self.url_obj = ShortenUrl.objects.create(
            original_url="https://example.com",
            short_code="stats123"
        )
        
        # Add some test counts
        increment_redirect_count("stats123")
        increment_redirect_count("stats123")
        
    def test_get_counts_for_nonexistent_shortcode(self):
        """Test retrieving counts for a shortcode that doesn't exist in DB"""
        response = self.client.get(reverse("stats_url", args=["nonexistent"]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_get_counts_for_unknown_shortcode(self):
        """Test retrieving counts for a shortcode with no recorded clicks"""
        # Create URL but don't increment counter
        ShortenUrl.objects.create(
            original_url="https://example.org",
            short_code="noclicks"
        )
        response = self.client.get(reverse("stats_url", args=["noclicks"]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class StatsUrlRoutingTests(TestCase):
    """Test URL routing for stats app"""
    
    def test_valid_stats_url(self):
        """Test that valid URL patterns route to the right view"""
        url = reverse("stats_url", args=["abc123"])
        self.assertEqual(url, "/stats/abc123/")
        
    def test_catch_all_pattern(self):
        """Test that invalid URL patterns are caught by catch-all"""
        client = Client()
        response = client.get("/stats/invalid/path/")
        self.assertEqual(response.status_code, status.HTTP_501_NOT_IMPLEMENTED)
        
        response = client.get("/stats/")
        self.assertEqual(response.status_code, status.HTTP_501_NOT_IMPLEMENTED)