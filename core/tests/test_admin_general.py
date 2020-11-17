import pytest

from django.apps import apps

from core.models import BasePHistorical
from core.tests.utils import get_factory


def get_params():
    return [
        (m._meta.app_label, m._meta.model_name, get_factory(m))  # noqa
        for m in filter(
            lambda x: issubclass(x, BasePHistorical),
            apps.get_models()
        )
    ]


@pytest.fixture(params=get_params())
def model_params(request):
    return request.param


def test_admin_general_changelist(model_params, test_page_status):
    app_label, model_name, factory = model_params
    factory.create_batch(size=10)
    page_name = f'admin:{app_label}_{model_name}_changelist'
    test_page_status(page_name)


def test_admin_general_change(model_params, test_page_status):
    app_label, model_name, factory = model_params
    obj = factory()
    page_name, kw = (f'admin:{app_label}_{model_name}_change',  # noqa
                     {'object_id': obj.pk})
    test_page_status(page_name, **kw)


def test_admin_general_delete(model_params, test_page_status):
    app_label, model_name, factory = model_params
    obj = factory()
    page_name, kw = (f'admin:{app_label}_{model_name}_delete',  # noqa
                     {'object_id': obj.pk})
    test_page_status(page_name, **kw)


def test_admin_general_add(model_params, test_page_status):
    app_label, model_name, __ = model_params
    page_name = f'admin:{app_label}_{model_name}_add'
    test_page_status(page_name)
