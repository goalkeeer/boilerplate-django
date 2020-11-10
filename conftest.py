import os
from contextlib import contextmanager

import pytest
from django import setup as django_setup
from django.core.cache import caches
from django.test import TransactionTestCase


# Transaction rollback emulation
# http://docs.djangoproject.com/en/2.0/topics/testing/overview/#rollback-emulation
TransactionTestCase.serialized_rollback = True


@pytest.fixture
def api_user():
    from django.contrib.auth import get_user_model
    user_model = get_user_model()
    user = user_model(username='test', email='test@test.ru', is_active=True)
    user.set_password('test_password')
    user.save()
    return user


def pytest_configure():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "_project_.settings")
    django_setup()


@pytest.fixture(scope='session')
def base_url(live_server):
    return live_server.url


@pytest.fixture(autouse=True)
def clear_caches():
    for cache in caches.all():
        cache.clear()


# HELPERS

@pytest.fixture(scope='function')
def assert_num_queries_lte(pytestconfig):
    from django.db import connection
    from django.test.utils import CaptureQueriesContext

    @contextmanager
    def _assert_num_queries(num):
        with CaptureQueriesContext(connection) as context:
            yield
            queries = len(context)
            if queries > num:
                msg = f"Expected to perform less then {num} queries" \
                      f" but {queries} were done"
                if pytestconfig.getoption('verbose') > 0:
                    sqls = (q['sql'] for q in context.captured_queries)
                    msg += '\n\nQueries:\n========\n\n%s' % '\n\n'.join(sqls)
                else:
                    msg += " (add -v option to show queries)"
                pytest.fail(msg)

    return _assert_num_queries
