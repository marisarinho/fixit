from django.test import TestCase


class HealthCheckTests(TestCase):
    def test_health_page_returns_success(self):
        response = self.client.get("/health/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "FixIt está no ar.")
