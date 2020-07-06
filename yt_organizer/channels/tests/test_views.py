from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from model_bakery import baker

from channels.models import Category


class CategoryDetailAccessTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("user", "user@test.com", "userpassword")
        self.public_category = baker.make(Category, public=True, user=self.user)
        self.private_category = baker.make(Category, public=False, user=self.user)

    def test_access_public_category_without_authenticated(self):
        url = reverse(
            "channels:category_details",
            args=(self.user.username, self.public_category.slug,),
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_access_private_category_without_authenticated(self):
        url = reverse(
            "channels:category_details",
            args=(self.user.username, self.private_category.slug,),
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_access_private_category_authenticated(self):
        self.client.login(username=self.user.username, password="userpassword")
        url = reverse(
            "channels:category_details",
            args=(self.user.username, self.private_category.slug,),
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_access_private_category_authenticated_with_other_user(self):
        other_user = User.objects.create_user(
            "otheruser", "otheruser@test.com", "otheruserpassword"
        )
        self.client.login(username=other_user.username, password="otheruserpassword")

        url = reverse(
            "channels:category_details",
            args=(self.user.username, self.private_category.slug,),
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_access_category_that_does_not_exists(self):
        url = reverse(
            "channels:category_details",
            args=(self.user.username, "this-slug-does-not-exist"),
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_access_user_that_does_not_exists(self):
        url = reverse(
            "channels:category_details",
            args=("this-user-does-not-exist", self.public_category.slug),
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_access_public_category_without_authenticated(self):
        url = reverse(
            "channels:category_details",
            args=(self.user.username, self.public_category.slug,),
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
