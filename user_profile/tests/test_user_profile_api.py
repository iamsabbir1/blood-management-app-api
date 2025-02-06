"""
Tests for user_profile api
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


from rest_framework import status
from rest_framework.test import APIClient


from core.models import Profile
from user_profile.serializers import ProfileSerializer

PROFILE_URL = reverse("user_profile:profile")
PROFILE_CREATE_URL = reverse("user_profile:profile-create")


def create_user_profile(user, **params):
    """Create and return a sample user_profile"""
    defaults = {
        "name": "John Doe",
        "contact": "+8801738392320",
        "blood_group": "O+",
        "is_donor": "False",
    }

    defaults.update(params)
    profile = Profile.objects.create(
        user=user,
        **defaults,
    )
    return profile


class PublicProfileAPITests(TestCase):
    """Test unauthenticated API request"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call the API"""

        res = self.client.get(PROFILE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateProfileAPITests(TestCase):
    """Test API requests that require authentication."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@example.com",
            password="testpass123",
        )
        self.client.force_authenticate(self.user)

    def test_create_profile_for_user(self):
        """Test creating a profile for a user."""

        payload = {
            "name": "John Doe",
            "contact": "12353224",
            "blood_group": "O+",
            "is_donor": True,
        }

        res = self.client.post(PROFILE_CREATE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        profile = Profile.objects.get(user=self.user)

        for key in payload.keys():
            self.assertEqual(getattr(profile, key), payload[key])

    def test_retrieve_profile_success(self):
        """Test retrieveing profile for logged in user"""
        create_user_profile(user=self.user)
        res = self.client.get(PROFILE_URL)

        profile = Profile.objects.get(user=self.user)
        serializer = ProfileSerializer(profile)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_user_cannot_have_multiple_profiles(self):
        """Test that a user cannot have multiple profiles"""

        user = get_user_model().objects.create_user(
            email="test1@example.com",
            password="testpass123",
        )

        Profile.objects.create(
            user=user,
            name="John Doe",
            contact="1234567890",
            blood_group="O+",
            is_donor=True,
        )

        with self.assertRaises(Exception):
            Profile.objects.create(
                user=user,
                name="Jane Doe",
                contact="0987654321",
                blood_group="A+",
                is_donor=False,
            )

    # def test_update_is_typing(self):
    #     """Test updating is_typing."""

    #     user = get_user_model().objects.create_user(
    #         email="test1@example.com",
    #         password="testpass123",
    #     )

    #     Profile.objects.create()
