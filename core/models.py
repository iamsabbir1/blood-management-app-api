"""
Database models
"""

from django.conf import settings

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, password=None, **extra_fields):
        """Create save and return a new user."""
        if not email:
            raise ValueError("User must have an email address.")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and save superuser."""

        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""

    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class Profile(models.Model):
    """Profile Object"""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    name = models.CharField(max_length=255, null=False)
    contact = models.CharField(max_length=15, null=False)
    blood_group = models.CharField(max_length=5)
    is_donor = models.BooleanField(default=False)
    is_contact_hidden = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    was_recently_active = models.BooleanField(default=False)
    last_active = models.DateTimeField(null=True, blank=True)
    is_typing = models.BooleanField(default=False)

    def __str__(self):
        return self.name
