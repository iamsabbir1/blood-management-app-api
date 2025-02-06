# views.py
"""
Views for the profile API
"""

import logging

from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from core.models import Profile
from user_profile import serializers


logger = logging.getLogger(__name__)


class ProfileViewSet(generics.RetrieveAPIView):
    """Manage the authenticated user's profile"""

    serializer_class = serializers.ProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user's profile"""
        return Profile.objects.get(user=self.request.user)


class ProfileCreateView(generics.CreateAPIView):
    """Create a new profile for the authenticated user."""

    serializer_class = serializers.ProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Create a new profile for authenticated user."""
        if Profile.objects.filter(user=self.request.user).exists():
            """Raise error."""
            logger.error("A profile already exists.")
            raise ValidationError("A profile already exists for this user.")
        serializer.save(user=self.request.user)
