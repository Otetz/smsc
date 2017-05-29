# -*- coding: utf-8 -*-
"""
smsc.responses module.

This module contains the responses objects wrapping SMSC.ru API answers.

:copyright: (c) 2017 by Alexey Shevchenko.
:license: MIT, see LICENSE for more details.
"""
from abc import ABCMeta

from collections import namedtuple
from typing import Any, Dict, Optional

from arrow import get as arrow_get
from dateutil.tz import tz


# noinspection PyUnresolvedReferences
class SMSCError(namedtuple("SMSCError", ["code", "error"])):
    """
    Named tuple for error description with code.

    :param int code: Code of error
    :param str error: Description of error
    """


class Status:
    """
    Message delivery status with identification.

    :param dict obj: Dictionary from API JSON response
    """

    def __init__(self, obj: Dict[str, Any]) -> None:  # noqa: D102
        self.__id = int(obj.get("status", 0))
        self.__name = str(obj.get("status_name", ""))
        for name in ["status", "status_name"]:
            del obj[name]

    def __str__(self) -> str:
        """Represent object as string."""
        return "<%s status=%d name=%s>" % (self.__class__.__name__, self.__id, self.__name)

    def __repr__(self) -> str:
        """Represent object for debug purposes."""
        return str(self)

    @property
    def status_id(self) -> int:
        """Id of delivery status."""
        return self.__id

    @property
    def name(self) -> str:
        """Delivery status description."""
        return self.__name


class Response(metaclass=ABCMeta):
    """
    Basic class for response wrappers.

    :param dict obj: Dictionary from API JSON response
    """

    def __init__(self, obj: Dict[str, Any]) -> None:  # noqa: D102
        self.__error = obj.get("error", None)
        self.__code = int(obj.get("error_code", 0))

    @property
    def error(self) -> Optional[SMSCError]:
        """Error in response, if present."""
        if not self.__error and not self.__code:
            return None
        # noinspection PyTypeChecker
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
        self.__cost = float(obj.get("cost", 0.0))

    def __str__(self) -> str:
        """Represent object as string."""
        return "<%s id=%s count=%d cost=%.2f>" % (
            self.__class__.__name__, self.__id, self.__cnt, self.__cost)

    def __repr__(self) -> str:
        """Represent object for debug purposes."""
        return str(self)

    @property
    def message_id(self) -> str:
        """Id of sent message."""
        return self.__id

    @property
    def count(self) -> int:
        """Count of billed message parts."""
        return self.__cnt

    @property
    def cost(self) -> float:
        """Cost of sent message."""
        return self.__cost


class CostResponse(Response):
    """
    Response for get cost (send variation) API command.

    :param dict obj: Dictionary from API JSON response
    """

    def __init__(self, obj: Dict[str, Any]) -> None:  # noqa: D102
        super().__init__(obj)
        self.__cnt = int(obj.get("cnt", 0))
        self.__cost = float(obj.get("cost", 0.0))

    def __str__(self):
        """Represent object as string."""
        return "<%s count=%d cost=%.2f>" % (
            self.__class__.__name__, self.__cnt, self.__cost)

    def __repr__(self) -> str:
        """Represent object for debug purposes."""
        return str(self)

    @property
    def count(self) -> int:
        """Count of billed message parts."""
        return self.__cnt

    @property
    def cost(self) -> float:
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

    def __str__(self) -> str:
        """Represent object as string."""
        return "<%s id=%d status= %s>" % (self.__class__.__name__, self.__data["id"], self.__status)

    def __repr__(self) -> str:
        """Represent object for debug purposes."""
        return str(self)

    @property
    def status(self) -> Status:
        """Message delivery status with identification."""
        return self.__status

    @property
    def data(self) -> Dict[str, Any]:
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
        self.__credit = float(obj.get("credit", 0.0))
        self.__currency = str(obj.get("currency", ""))

    def __str__(self) -> str:
        """Represent object as string."""
        return "<%s balance=%.2f credit=%.2f currency=%s>" % (
            self.__class__.__name__, self.__balance, self.__credit, self.__currency)

    def __repr__(self) -> str:
        """Represent object for debug purposes."""
        return str(self)

    @property
    def balance(self) -> float:
        """Actual account balance."""
        return self.__balance

    @property
    def credit(self) -> float:
        """Available credit of account (if applied)."""
        return self.__credit

    @property
    def currency(self) -> str:
        """Currency for current account."""
        return self.__currency
