# -*- coding: utf-8 -*-
"""
SMSC.ru API Library.

Smsc is an library to send messages through SMSC.ru HTTP API.
Basic usage:

    >>> from smsc.messages import SMSMessage
    >>> from smsc.api import SMSC
    >>> client = SMSC(login='alexey', password='psw')
    >>> res = client.send(to='79999999999', message=SMSMessage(text='Hello, World!'))  # doctest: +SKIP
    >>> res.count # doctest: +SKIP
    1
    >>> res.cost # doctest: +SKIP
    1.44

The some other API methods are supported - see `smsc.api`. Full documentation is at
`Read the Docs <http://smsc_python.readthedocs.io/en/latest/>`_.

:copyright: (c) 2017 by Alexey Shevchenko.
:license: MIT, see LICENSE for more details.
"""

import logging  # noqa: T005
import sys  # noqa: T005

# noinspection PyUnresolvedReferences
from .api import SMSC  # noqa: F401
# noinspection PyUnresolvedReferences
from .responses import SendResponse, CostResponse, StatusResponse, BalanceResponse, Status  # noqa: F401
# noinspection PyUnresolvedReferences
from .messages import SMSMessage, FlashMessage, ViberMessage  # noqa: F401
# noinspection PyUnresolvedReferences
from .exceptions import SMSCException, SendError, GetCostError, GetBalanceError, GetStatusError  # noqa: F401

# Set default logging handler to avoid "No handler found" warnings.
try:  # Python 2.7+
    if sys.version_info >= (2, 7):
        from logging import NullHandler
except ImportError:
    if sys.version_info < (2, 7):
        class NullHandler(logging.Handler):
            """
            NullHandler implementation for Python < 2.7.

            This handler does nothing. It's intended to be used to avoid the
            "No handlers could be found for logger XXX" one-off warning. This is
            important for library code, which may contain code to log events. If a user
            of the library does not configure logging, the one-off warning might be
            produced; to avoid this, the library developer simply needs to instantiate
            a NullHandler and add it to the top-level logger of the library module or
            package.
            """

            def emit(self, record):
                """Stub."""

logging.getLogger(__name__).addHandler(NullHandler())
