Currency Converter
==================

A simple currency converter with caching for offline usage.

Installation
------------

Install it ``pipsi``:

.. code-block:: bash

    pipsi install currency-converter

This will install ``currency-converter`` to your ``$PATH`` which might be too long winded for you, an alias

.. code-block:: bash

    alias cc=currency-converter

Usage
-----

.. code-block:: bash

    $ currency-converter 100 usd gbp
    63.82 GBP

    $ currency-converter 100 usd gbp -- default
    63.82 GBP

    $ currency-converter 100 usd
    63.82 GBP


Running Tests
-------------

## TODO
* sorted imports
* travis
* 100% coverage??
* mock cache file with faked file
