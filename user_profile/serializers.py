"""
Serializers for profile api
"""

from rest_framework import serializers
from core.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for Profile"""

    class Meta:
        model = Profile
        fields = [
            "name",
            "contact",
            "blood_group",
            "is_donor",
            "is_contact_hidden",
            "is_online",
            "was_recently_active",
            "last_active",
            "is_typing",
        ]
