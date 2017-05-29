SMSC
====

.. image:: https://img.shields.io/pypi/v/smsc.svg
    :target: https://pypi.python.org/pypi/smsc

.. image:: https://readthedocs.org/projects/smsc_python/badge/?version=latest
    :target: http://smsc_python.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://travis-ci.org/Otetz/smsc.svg?branch=master
    :target: https://travis-ci.org/Otetz/smsc

.. image:: https://coveralls.io/repos/github/Otetz/smsc/badge.svg?branch=master
    :target: https://coveralls.io/github/Otetz/smsc?branch=master

.. image:: https://img.shields.io/codeclimate/github/Otetz/smsc.svg
    :target: https://codeclimate.com/github/Otetz/smsc

.. image:: https://img.shields.io/pypi/l/smsc.svg
    :target: https://pypi.python.org/pypi/smsc

.. image:: https://img.shields.io/pypi/pyversions/smsc.svg
    :target: https://pypi.python.org/pypi/smsc

SMSC.ru HTTP API Library.

Installation
------------

Install smsc package from `PyPI <https://pypi.python.org/pypi>`_:

.. code-block:: bash

    $ pip install smsc

Getting started
---------------

Basic usage sample:

.. code-block:: python

    >>> from smsc.messages import SMSMessage
    >>> from smsc.api import SMSC
    >>> client = SMSC(login='alexey', password='psw')
    >>> res = client.send(to='79999999999', message=SMSMessage(text='Hello, World!'))
    >>> res.count
    1
    >>> res.cost
    1.44

Documentation
-------------

Documentation is available at `Read the Docs <http://smsc_python.readthedocs.io/en/latest/>`_.

Links
-----

- `SMSC.ru HTTP API <https://smsc.ru/api/http/#menu>`_
