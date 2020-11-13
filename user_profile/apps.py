from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import gettext_lazy as _


class AppConfig(BaseAppConfig):
    name = 'user_profile'
    verbose_name = _('Пользователи и группы')

    def ready(self):
        from . import signals
        assert signals  # noqa unused import
