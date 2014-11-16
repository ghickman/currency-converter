import os
import unittest.mock

import pytest
import requests
from click.testing import CliRunner

from currency_converter.main import (cached_rate, cli, convert,
                                     get_conversion_rate, google_rate)


@pytest.fixture
def fake_cache():
    """Build a fake cache dictionary."""
    return {('usd', 'gbp'): 0.6}


@pytest.yield_fixture
def fake_html():
    """
    Create a fake requests response.

    Uses a stand python file descriptor with a couple of extra methods to
    look like a requests Response.
    """
    path = os.path.dirname(os.path.realpath(__file__))
    f = open(os.path.join(path, 'fake_output.html'), 'r')
    f.ok = True
    f.text = f.read()
    yield f
    f.close()


@pytest.fixture
def patch_write_cache():
    """
    Make `write_cache` a noop.

    Useful when we don't care about writing out the cache.
    """
    w_cache = 'currency_converter.main.write_cache'
    return unittest.mock.patch(w_cache, lambda x, y: str)


@pytest.fixture
def patch_get_cache(fake_cache):
    """Mock `get_cache` and return a known cache dictionary."""
    g_cache = 'currency_converter.main.get_cache'
    return unittest.mock.patch(g_cache, lambda: fake_cache)


@pytest.fixture
def test_cache_rate(fake_cache):
    """Test cache rate returns a known item from the cache."""
    g_cache = 'currency_converter.main.get_cache'
    with unittest.mock.patch(g_cache, lambda: fake_cache):
        assert cached_rate('usd', 'gbp') == 0.6


def test_cli(fake_html):
    """Check a successful run of the CLI."""
    runner = CliRunner()
    with unittest.mock.patch('requests.get', lambda x, timeout: fake_html):
        result = runner.invoke(cli, ['100', 'usd', 'gbp'])
    assert result.exit_code == 0
    assert result.output == '63.82 GBP\n'


def test_conversion_rate_error_checking():
    """Passing in the same currency should return a converstion rate of 1.0."""
    assert get_conversion_rate(42, 42) == 1.0


def test_convert():
    """Check a successful call of `convert`."""
    g_rate = 'currency_converter.main.google_rate'
    with unittest.mock.patch(g_rate, lambda x, y: float(0.6382)):
        assert convert(150, 'usd', 'gbp') == (95.73, 'gbp')


def test_convert_no_to_currency(fake_html):
    """Check the use of default currency."""
    get_cache = 'currency_converter.main.get_cache'
    with unittest.mock.patch(get_cache, lambda: {'fav': 'test'}):
        with unittest.mock.patch('requests.get', lambda x, timeout: fake_html):
            assert convert(150, 'usd') == (95.73, 'test')


def test_fallback_to_cached_rate_on_api_error(patch_write_cache,
                                              patch_get_cache):
    """Check the cached rate value is used when the API doesn't respond."""
    mock = unittest.mock.Mock()
    mock.side_effect = requests.exceptions.HTTPError()
    with patch_write_cache:
        g_rate = 'currency_converter.main.google_rate'
        with unittest.mock.patch(g_rate, new=mock):
            with patch_get_cache:
                rate = get_conversion_rate('usd', 'gbp')
    assert rate == 0.6


def test_fallback_to_cached_rate_when_rate_not_found_in_response(patch_write_cache,
                                                                 patch_get_cache):
    """Check the cached rate value is retured when a rate can't be parsed from the API response."""
    mock = unittest.mock.Mock()
    mock.side_effect = AttributeError()
    with patch_write_cache:
        g_rate = 'currency_converter.main.google_rate'
        with unittest.mock.patch(g_rate, new=mock):
            with patch_get_cache:
                rate = get_conversion_rate('usd', 'gbp')
    assert rate == 0.6


def test_google_rate(fake_html):
    """Test `google_rate` correctly gets the value from the HTML document."""
    with unittest.mock.patch('requests.get', lambda x, timeout: fake_html):
        rate = google_rate('USD', 'GBP')
    assert rate == float(0.6382)
