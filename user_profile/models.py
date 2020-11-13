from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group as DjangoGroup

from core.models import SoftDeleted, BasePHistorical

from .managers import (
    SoftObjectsUserManager, AllObjectsUserManager,
    SoftDeletedObjectsUserManager
)


class User(SoftDeleted, AbstractUser, BasePHistorical):
    # username uniqueness in Meta.constraints
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Обязательное. 150 символов или меньше.'
                    ' Разрешается использовать буквы, цифры и @/./+/-/_.'),
        validators=[AbstractUser.username_validator],
        error_messages={
            'unique': _("Пользователь с таким логином уже существует."),
        },
    )
    middle_name = models.CharField(
        _('Отчество'), max_length=150,
        blank=True, null=True
    )

    objects = SoftObjectsUserManager()
    all_objects = AllObjectsUserManager()
    deleted_objects = SoftDeletedObjectsUserManager()

    @property
    def is_deleted(self):
        return bool(self.deleted)

    @classmethod
    def normalize_username(cls, username):
        username = super().normalize_username(username)
        return username.lower()

    class Meta:
        verbose_name = _('пользователь')
        verbose_name_plural = _('пользователи')
        ordering = ['-updated']


# We want to change Groups through this app admin
class Group(DjangoGroup):
    class Meta:
        verbose_name = _('group')
        verbose_name_plural = _('groups')
        proxy = True
