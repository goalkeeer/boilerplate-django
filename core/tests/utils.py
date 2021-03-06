import importlib

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission


def add_user_permissions(user, model, *actions):
    ctype = ContentType.objects.get_for_model(model)
    user.user_permissions.add(*(
        Permission.objects.get(codename=f'{action}_{model.__name__.lower()}',
                               content_type=ctype)
        for action in actions
    ))


def add_admin_access_permission(user):
    user.is_staff = True
    user.save()


def create_permission(model_name, perm_name, perm_codename):
    content_type = ContentType.objects.get(model=model_name)
    permission = Permission.objects.create(
        name=perm_name, content_type=content_type,
        codename=perm_codename)
    return permission


def get_factory(model):
    module = model._meta.app_label  # noqa
    name = model.__name__
    try:
        factories_module = importlib.import_module(f'{module}.tests.factories')
    except ModuleNotFoundError:
        raise Exception(f'App "{module}" does not has module "factories".')
    try:
        return getattr(factories_module, f'{name}Factory')
    except AttributeError:
        raise Exception(f'Model "{name}" does not has factory.')
