from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from .models import URL


class AuthTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass")
        self.token_url = reverse("token_obtain_pair")
        self.refresh_url = reverse("token_refresh")

    def test_obtain_jwt_token(self):
        response = self.client.post(
            self.token_url, {"username": "testuser", "password": "testpass"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_refresh_jwt_token(self):
        response = self.client.post(
            self.token_url, {"username": "testuser", "password": "testpass"})
        refresh_token = response.data["refresh"]

        response = self.client.post(
            self.refresh_url, {"refresh": refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)


class URLTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass")
        token_url = reverse("token_obtain_pair")
        response = self.client.post(
            token_url, {"username": "testuser", "password": "testpass"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.access_token = response.data["access"]
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.access_token)

        self.url_list_create = reverse("url-list")

    def test_create_delete_url(self):
        data = {
            "orig_url": "https://example.com"
        }
        response = self.client.post(self.url_list_create, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(URL.objects.count(), 1)
        self.assertEqual(URL.objects.get().orig_url, "https://example.com")
        self.assertIn("shorted_url", response.data)

        self.url_delete = self.url_list_create + \
            str(response.data.get("id")) + "/"
        response = self.client.delete(self.url_delete)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(URL.objects.count(), 0)
