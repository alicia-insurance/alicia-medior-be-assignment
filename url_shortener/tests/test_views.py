import yaml
from pathlib import Path
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from url_shortener.models import ShortURL
from parameterized import parameterized
from functools import cached_property

class BaseTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    @cached_property
    def scenarios(self):
        yaml_path = Path(__file__).parent / 'fixtures' / 'url_shortener.yml'
        with open(yaml_path, 'r') as file:
            return yaml.safe_load(file)

    def execute_request(self, scenario, **url_params):
        endpoint = scenario.get('endpoint', '')
        if url_params:
            endpoint = endpoint.format(**url_params)

        method = scenario['type'].lower()
        request_data = scenario.get('request', {}).get('body', {})

        http_method = getattr(self.client, method)
        return http_method(endpoint, request_data, format='json')

    def validate_response(self, response, expected):
        # Verify status code
        self.assertEqual(response.status_code, expected['status_code'])

        # Verify contains fields
        if 'contains' in expected:
            for field in expected['contains']:
                self.assertIn(field, response.data)

        # Verify exact matches
        if 'match' in expected:
            for field, value in expected['match'].items():
                self.assertEqual(response.data[field], value)

class URLShortenerViewTests(BaseTestCase):
    @parameterized.expand([
        "Test creating short URL",
        "Test custom alias creation",
        "Test invalid URL format",
        "Test empty URL",
    ])
    def test_url_shortener_scenarios(self, scenario_name):
        scenario = next(
            (s for s in self.scenarios if s['scenario'] == scenario_name),
            None
        )
        if not scenario:
            self.fail(f"Scenario '{scenario_name}' not found in YAML file")

        response = self.execute_request(scenario)
        self.validate_response(response, scenario['expected_response'])


class URLStatsViewTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.url = ShortURL.objects.create(
            original_url='https://www.example.com',
            short_alias='test123',
            access_count=5
        )

    @parameterized.expand([
        "Test URL statistics",
    ])
    def test_stats_scenarios(self, scenario_name):
        scenario = next(
            (s for s in self.scenarios if s['scenario'] == scenario_name),
            None
        )
        if not scenario:
            self.fail(f"Scenario '{scenario_name}' not found in YAML file")

        response = self.execute_request(scenario, short_code=self.url.short_alias)
        self.validate_response(response, scenario['expected_response'])


class URLRedirectViewTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.url = ShortURL.objects.create(
            original_url='https://www.example.com',
            short_alias='redirect123'
        )

    @parameterized.expand([
        "Test URL redirect",
    ])
    def test_redirect_scenarios(self, scenario_name):
        scenario = next(
            (s for s in self.scenarios if s['scenario'] == scenario_name),
            None
        )
        if not scenario:
            self.fail(f"Scenario '{scenario_name}' not found in YAML file")

        response = self.execute_request(scenario, short_code=self.url.short_alias)
        self.validate_response(response, scenario['expected_response'])

        # Check access count increment
        updated_url = ShortURL.objects.get(pk=self.url.pk)
        self.assertEqual(updated_url.access_count, 1)