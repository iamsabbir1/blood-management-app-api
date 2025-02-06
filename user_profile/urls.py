"""
URL mappings for user_profile app
"""

from django.urls import path, include

from rest_framework.routers import DefaultRouter
from user_profile import views


# router = DefaultRouter()
# router.register("profile", views.ProfileViewSet, basename="profile")


app_name = "user_profile"
urlpatterns = [
    path("profile/", views.ProfileViewSet.as_view(), name="profile"),
    path("profile/create/", views.ProfileCreateView.as_view(), name="profile-create"),
    # path("profile/", include(router.urls)),
]
