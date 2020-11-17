import pytest

from django.apps import apps
from django.utils.text import camel_case_to_spaces

from core.models import BasePHistorical
from core.tests.utils import get_factory


def get_params():
    return [
        (model, get_factory(model))
        for model in filter(
            lambda x: issubclass(x, BasePHistorical),
            apps.get_models()
        )
    ]


@pytest.fixture(params=get_params())
def model_and_factory(request):
    return request.param


def test_create_model_by_factory(model_and_factory):
    model, factory = model_and_factory
    obj1 = factory.create()
    obj2 = model.objects.get()
    assert obj1.uid == obj2.uid
    assert str(obj1) == str(obj2)


def test_critical_model_meta(model_and_factory):
    model, _ = model_and_factory  # noqa
    assert hasattr(model._meta, 'verbose_name')  # noqa
    assert model._meta.verbose_name != camel_case_to_spaces(  # noqa
        model._meta.object_name)  # noqa
    assert hasattr(model._meta, 'verbose_name_plural')  # noqa
    assert model._meta.verbose_name_plural != f'{model._meta.verbose_name}s'  # noqa


def test_critical_model_protocol(model_and_factory):
    model, _ = model_and_factory
    fields = [field.name for field in model._meta.get_fields()]  # noqa
    assert hasattr(model, 'history')
    assert 'uid' in fields
    assert 'version' in fields
    assert 'created' in fields
    assert 'updated' in fields
    assert 'deleted' in fields
