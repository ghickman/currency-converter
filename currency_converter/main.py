# -*- coding: utf-8 -*-

import re

import click
import requests

from .cache import get_cache, write_cache


def cached_rate(from_currency, to_currency):
    """Attempt to get a conversion rate from the cache."""
    return get_cache().get((from_currency, to_currency), 0.0)


def google_rate(from_currency, to_currency):
    """
    Get the conversion rate from Google.

    Returns the conversion rate as a float.
    """
    url = 'https://www.google.com/finance/converter?a={}&from={}&to={}'
    r = requests.get(url.format(1, from_currency, to_currency), timeout=5)
    if not r.ok:
        return r.raise_for_status()

    # get the rate (and currency) from the page
    pattern = re.compile(r'<span class=bld>(.*)<\/span>')
    return float(re.search(pattern, r.text).group(1).split(' ')[0])


def get_conversion_rate(from_currency, to_currency):
    """
    Get the conversion rate for the given currencies.

    A conversion rate is requested instead of the conversion so the local
    cache can be updated for offline usage.
    """
    if from_currency == to_currency:
        return 1.0

    try:
        rate = google_rate(from_currency, to_currency)
    except (requests.exceptions.HTTPError, AttributeError) as e:
        print(e)
        return cached_rate(from_currency, to_currency)
    else:
        write_cache((from_currency, to_currency), rate)
        return rate


def convert(amount, from_currency, to_currency=None):
    """
    Convert one currency quantity to another.

    Return a float of the amount in the requested currency.
    """
    if to_currency is None:
        to_currency = get_cache().get('fav')

    rate = get_conversion_rate(from_currency, to_currency)

    return amount * rate, to_currency


@click.command()
@click.argument('amount', type=float)
@click.argument('from_currency')
@click.argument('to_currency', envvar='TO_CURR', default=get_cache().get('fav'))
@click.option('--default', is_flag=True, help='Set your default currency to the TO_CURRENCY')
def cli(amount, from_currency, to_currency, default):
    """Convert from one currency to another."""
    amount, to_currency = convert(amount, from_currency, to_currency)
    click.echo('{} {}'.format(amount, to_currency.upper()))

    if default:
        write_cache('fav', to_currency)
