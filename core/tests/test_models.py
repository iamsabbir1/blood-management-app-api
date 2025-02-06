"""
Test for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = "test@example.com"
        password = "testpass123"

        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test new user with normalized email"""

        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "Sample123")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "test123")

    def test_create_superuser(self):
        """Test creating a superuser"""

        user = get_user_model().objects.create_superuser(
            "test@example.com",
            "test123",
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


class ProfileModelTests(TestCase):
    """Test creating a profile for a user"""

    def test_create_profile(self):
        user = get_user_model().objects.create_user(
            email="test@example.com",
            password="testpass123",
        )

        profile = models.Profile.objects.create(
            user=user,
            name="John Doe",
            contact="+8801783938172",
            blood_group="AB+",
            is_donor=True,
            is_contact_hidden=False,
            is_online=False,
            was_recently_active=False,
            last_active=None,
            is_typing=False,
        )

        self.assertEqual(str(profile), profile.name)


class DonationHistoryModelTests(TestCase):
    """Test creating a DonationHistory Model"""

    def test_create_donation_history_when_is_donor_true(self):
        user = get_user_model().objects.create_user(
            email="test@example.com",
            password="testpass123",
        )

        profile = models.Profile.objects.create(
            user=user,
            name="John Doe",
            contact="+8801783938172",
            blood_group="AB+",
            is_donor=True,
            is_contact_hidden=False,
            is_online=False,
            was_recently_active=False,
            last_active=None,
            is_typing=False,
        )

        donation_history = models.DonationHistory.objects.create(
            profile=profile,
            total_donations=0,
            last_donation_date="10-02-2023",
            can_donate=True,
            is_going_to_donate=False,
        )

        self.assertEqual(donation_history.profile, profile)
        self.assertEqual(donation_history.total_donations, 0)
        self.assertEqual(donation_history.donation_date, "10-02-2023")

    def test_dont_create_donation_history_when_is_donor_false(self):
        """Test no donation history is created when is_donor is False"""

        user = get_user_model().objects.create_user(
            email="test@example.com",
            password="testpass123",
        )

        profile = models.Profile.objects.create(
            user=user,
            name="John Doe",
            contact="+8801348920394",
            blood_group="A+",
            is_donor=False,
        )

        with self.assertRaises(ValueError):
            models.DonationHistory.obects.create(
                profile=profile,
                total_donations=0,
                last_donation_date="10-02-2023",
                can_donate=True,
                is_going_to_donate=False,
            )
