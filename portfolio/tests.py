from django.test import TestCase
from django.urls import reverse
class PortfolioSmokeTests(TestCase):
    def test_home_returns_200(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pravin Dayanand Bansode")
        self.assertContains(response, "Pics")
