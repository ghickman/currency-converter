import os
import unittest.mock

import pytest

from currency_converter.cache import get_cache


@pytest.fixture
def fake_cache():
    """
    Fixture for getting a fake cache path.

    Designed for use with `patch()` on the `get_cache_path` method.
    """
    path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(path, 'fake_cache.pickle')


def test_get_cache(fake_cache):
    """Test the cache successfully returns a dictionary."""
    get_cache_path = 'currency_converter.cache.get_cache_path'
    with unittest.mock.patch(get_cache_path, lambda: fake_cache):
        assert get_cache() == {'foo': 'bar'}


def test_get_missing_cache():
    """No cache file should cause the cache to return an empty dictionary."""
    get_cache_path = 'currency_converter.cache.get_cache_path'
    with unittest.mock.patch(get_cache_path, lambda: ''):
        assert get_cache() == {}
