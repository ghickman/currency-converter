Currency Converter
==================

A simple currency converter with caching for offline usage.

Installation
------------

Install it with ``pipsi``. If you're not using ``pipsi`` then you're missing out. Installation instructions are `here <https://github.com/mitsuhiko/pipsi#readme>`_.

.. code-block:: bash

    pipsi install currency-converter

This will install ``currency-converter`` to your ``$PATH`` which might be too long winded for you, you can also create an alias:

.. code-block:: bash

    alias cc=currency-converter


Usage
-----

There three main modes of usage: all options, set a default and use your default.

**All Options**
Specify how much to convert, the origin currency and the destination currency.

.. code-block:: bash

    $ currency-converter 100 usd gbp
    63.82 GBP


**Set a Default**
This works like the previous example but also writes the destination currency to the cache to save you having to specify it again.

.. code-block:: bash

    $ currency-converter 100 usd gbp -- default
    63.82 GBP


**Use the Default**
This method lets you take advantage of the default you set.

.. code-block:: bash

    $ currency-converter 100 usd
    63.82 GBP


Running Tests
-------------

.. code-block:: bash

    make test
