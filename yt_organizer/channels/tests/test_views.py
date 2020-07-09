import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from model_bakery import baker

from channels.models import Category, Channel, Video


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

    def test_access_public_category_of_another_user(self):
        other_user = User.objects.create_user(
            "otheruser", "otheruser@test.com", "otheruserpassword"
        )
        self.client.login(username=other_user.username, password="otheruserpassword")

        url = reverse(
            "channels:category_details",
            args=(self.user.username, self.public_category.slug,),
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class CategoryDetailTestCase(TestCase):
    def setUp(self):
        self.category = baker.make(Category, public=True)
        self.channel = baker.make(Channel)
        self.category.channels.add(self.channel)

    def test_context_has_list_of_videos(self):
        url = reverse(
            "channels:category_details",
            args=(self.category.user.username, self.category.slug,),
        )
        response = self.client.get(url)

        self.assertTrue("videos" in response.context)
        self.assertTrue(response.context["videos"] == [])

    def test_return_videos_of_category(self):
        published_date = timezone.now()
        videos = [
            baker.make(Video, channel=self.channel, published_date=published_date),
            baker.make(Video, channel=self.channel, published_date=published_date),
        ]

        url = reverse(
            "channels:category_details",
            args=(self.category.user.username, self.category.slug,),
        )
        response = self.client.get(url)

        self.assertTrue(response.context["videos"] == videos)

    def test_return_last_24h_videos_of_category_by_default(self):
        just_now = timezone.now()
        video_last_24h = baker.make(
            Video, channel=self.channel, published_date=just_now
        )

        older_than_24h = just_now - datetime.timedelta(hours=24, minutes=1)
        video_older_than_24h = baker.make(
            Video, channel=self.channel, published_date=older_than_24h
        )

        url = reverse(
            "channels:category_details",
            args=(self.category.user.username, self.category.slug,),
        )
        response = self.client.get(url)

        self.assertTrue(video_last_24h in response.context["videos"])
        self.assertTrue(video_older_than_24h not in response.context["videos"])

    def test_return_last_week_videos_of_category_if_query_string_week(self):
        last_week = timezone.now() - datetime.timedelta(days=7)
        older_than_week = last_week - datetime.timedelta(minutes=1)

        video_last_week = baker.make(
            Video, channel=self.channel, published_date=last_week
        )
        older_than_week_video = baker.make(
            Video, channel=self.channel, published_date=older_than_week
        )

        base_url = reverse(
            "channels:category_details",
            args=(self.category.user.username, self.category.slug,),
        )
        url = f"{base_url}?period=week"
        response = self.client.get(url)

        self.assertTrue(video_last_week in response.context["videos"])
        self.assertTrue(older_than_week_video not in response.context["videos"])

    def test_return_last_week_videos_of_category_if_query_string_all(self):
        last_week = timezone.now() - datetime.timedelta(days=7)
        older_than_week = last_week - datetime.timedelta(minutes=10)

        video_last_week = baker.make(
            Video, channel=self.channel, published_date=last_week
        )
        older_than_week_video = baker.make(
            Video, channel=self.channel, published_date=older_than_week
        )

        base_url = reverse(
            "channels:category_details",
            args=(self.category.user.username, self.category.slug,),
        )
        url = f"{base_url}?period=all"
        response = self.client.get(url)

        self.assertTrue(video_last_week in response.context["videos"])
        self.assertTrue(older_than_week_video in response.context["videos"])

    def test_return_videos_only_of_category(self):
        published_date = timezone.now()
        category_video = baker.make(
            Video, channel=self.channel, published_date=published_date
        )

        video_of_another_category = baker.make(
            Video, title="Video of another category", published_date=published_date
        )

        url = reverse(
            "channels:category_details",
            args=(self.category.user.username, self.category.slug,),
        )
        response = self.client.get(url)

        self.assertTrue(category_video in response.context["videos"])
        self.assertTrue(video_of_another_category not in response.context["videos"])
