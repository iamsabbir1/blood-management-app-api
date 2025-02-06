# views.py
"""
Views for the profile API
"""

from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Profile
from user_profile import serializers


class ProfileViewSet(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user's profile"""

    serializer_class = serializers.ProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user's profile"""
        return Profile.objects.get(user=self.request.user)
