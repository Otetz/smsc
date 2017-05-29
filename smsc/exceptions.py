# -*- coding: utf-8 -*-
"""
smsc.exceptions module.

This module contains the set of smsc' exceptions.

:copyright: (c) 2017 by Alexey Shevchenko.
:license: MIT, see LICENSE for more details.
"""


class SMSCException(Exception):
    """There was an ambiguous exception that occurred while handling your SMSC API request."""


class SendError(SMSCException):
    """A Send Message error occurred."""


class GetCostError(SMSCException):
    """A Get Cost error occurred."""


class GetStatusError(SMSCException):
    """A Get Status error occurred."""


class GetBalanceError(SMSCException):
    """A Get Balance error occurred."""
