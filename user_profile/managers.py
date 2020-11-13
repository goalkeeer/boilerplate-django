from django.contrib.auth.models import UserManager
from pik.core.models.soft_deleted import (
    SoftObjectsQuerySet, AllObjectsQuerySet, SoftDeletedObjectsQuerySet)


# We have to override User manager cause django requires some manager methods
# https://docs.djangoproject.com/en/3.0/topics/db/managers/#creating-a-manager-with-queryset-methods


class CustomUserMixin:
    use_in_migrations = True


class SoftObjectsUserManager(
        CustomUserMixin, UserManager.from_queryset(SoftObjectsQuerySet)):
    pass


class AllObjectsUserManager(
        CustomUserMixin, UserManager.from_queryset(AllObjectsQuerySet)):
    pass


class SoftDeletedObjectsUserManager(
        CustomUserMixin,
        UserManager.from_queryset(SoftDeletedObjectsQuerySet)):
    pass
