# -*- coding: utf-8 -*-
"""
smsc.responses module.

This module contains the responses objects wrapping SMSC.ru API answers.

:copyright: (c) 2017 by Alexey Shevchenko.
:license: MIT, see LICENSE for more details.
"""
from abc import ABCMeta

from collections import namedtuple
from typing import Any, Dict

from arrow import get as arrow_get
from dateutil.tz import tz


class SMSCError(namedtuple("SMSCError", ["code", "error"])):
    """Named tuple for error description with code."""


class Response(metaclass=ABCMeta):
    """
    Basic class for response wrappers.

    :param dict obj: Dictionary from API JSON response
    """

    def __init__(self, obj: Dict[str, Any]) -> None:  # noqa: D102
        self.__error = obj.get("error", None)
        self.__code = int(obj.get("error_code", 0))

    @property
    def error(self):
        """Error in response, if present."""
        if not self.__error and not self.__code:
            return None
        return SMSCError(self.__code, self.__error)


class SendResponse(Response):
    """
    Response for send API command.

    :param dict obj: Dictionary from API JSON response
    """

    def __init__(self, obj: Dict[str, Any]) -> None:  # noqa: D102
        super().__init__(obj)
        self.__id = obj.get("id", None)
        self.__cnt = int(obj.get("cnt", 0))
        self.__cost = obj.get("cost", None)

    def __str__(self):
        """Represent object as string."""
        return "<%s id=%s count=%d cost=%s>" % (
            self.__class__.__name__, self.__id, self.__cnt, self.__cost)

    @property
    def message_id(self):
        """Id of sent message."""
        return self.__id

    @property
    def count(self):
        """Count of billed message parts."""
        return self.__cnt

    @property
    def cost(self):
        """Cost of sent message."""
        return self.__cost


class CostResponse(Response):
    """
    Response for get cost (send variation) API command.

    :param dict obj: Dictionary from API JSON response
    """

    def __init__(self, obj: Dict[str, Any]) -> None:  # noqa: D102
        super().__init__(obj)
        self.__cnt = obj.get("cnt", None)
        self.__cost = obj.get("cost", None)

    def __str__(self):
        """Represent object as string."""
        return "<%s count=%d cost=%s>" % (
            self.__class__.__name__, self.__cnt, self.__cost)

    @property
    def count(self):
        """Count of billed message parts."""
        return self.__cnt

    @property
    def cost(self):
        """Cost of message."""
        return self.__cost


class StatusResponse(Response):
    """
    Response for get status API command.

    :param dict obj: Dictionary from API JSON response
    """

    def __init__(self, obj: Dict[str, Any]) -> None:  # noqa: D102
        super().__init__(obj)
        self.__status = Status(obj)
        self.__data = {}  # type: Dict[str, Any]
        for name in obj.keys():
            self.__data[name] = obj.get(name, None)
        if self.__data["last_date"] is not None:
            self.__data["last_date"] = arrow_get(self.__data["last_date"], "DD.MM.YYYY HH:mm:ss",
                                                 tzinfo=tz.gettz("Europe/Moscow")).datetime
        if self.__data["send_date"] is not None:
            self.__data["send_date"] = arrow_get(self.__data["send_date"], "DD.MM.YYYY HH:mm:ss",
                                                 tzinfo=tz.gettz("Europe/Moscow")).datetime
        for name in ["send_timestamp", "last_timestamp"]:
            del self.__data[name]

    def __str__(self):
        """Represent object as string."""
        return "<%s id=%d status= %s>" % (self.__class__.__name__, self.__data["id"], self.__status)

    def __repr__(self):
        """Represent object for debug purposes."""
        return str(self)

    @property
    def status(self):
        """Message delivery status with identification."""
        return self.__status

    @property
    def data(self):
        """Delivery status detailed data."""
        return self.__data


class BalanceResponse(Response):
    """
    Response for get account balance API command.

    :param dict obj: Dictionary from API JSON response
    """

    def __init__(self, obj: Dict[str, Any]) -> None:  # noqa: D102
        super().__init__(obj)
        self.__balance = float(obj.get("balance", 0.0))
        self.__credit = obj.get("credit", None)
        self.__currency = obj.get("currency", None)

    def __str__(self):
        """Represent object as string."""
        return "<%s balance=%.2f credit=%s currency=%s>" % (
            self.__class__.__name__, self.__balance, self.__credit, self.__currency)

    @property
    def balance(self):
        """Actual account balance."""
        return self.__balance

    @property
    def credit(self):
        """Available credit of account (if applied)."""
        return self.__credit

    @property
    def currency(self):
        """Currency for current account."""
        return self.__currency


class Status:
    """
    Message delivery status with identification.

    :param dict obj: Dictionary from API JSON response
    """

    def __init__(self, obj: Dict[str, Any]) -> None:  # noqa: D102
        self.__id = obj.get("status", None)
        self.__name = obj.get("status_name", None)
        for name in ["status", "status_name"]:
            del obj[name]

    def __str__(self):
        """Represent object as string."""
        return "<%s status=%d name=%s>" % (self.__class__.__name__, self.__id, self.__name)

    @property
    def status_id(self):
        """Id of delivery status."""
        return self.__id

    @property
    def name(self):
        """Delivery status description."""
        return self.__name
