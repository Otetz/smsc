# -*- coding: utf-8 -*-
"""
smsc.messages module.

This module contains the messages objects that power smsc library.

:copyright: (c) 2017 by Alexey Shevchenko.
:license: MIT, see LICENSE for more details.
"""
from abc import ABCMeta
from typing import Any, Dict, Optional


class Message(metaclass=ABCMeta):
    """
    Basic class for messages of ant type.

    Preferred for internal usage.

    :param str text: Text of the message
    :param Optional[str] msg_format: Message format. If None or empty - default, SMS message
    :param dict kwargs: Dictionary for optional API parameters
    """

    def __init__(self, text: str, msg_format: Optional[str] = None, **kwargs: dict) -> None:  # noqa: D102
        self._text = text
        self._format = msg_format
        self._translit = kwargs.get("translit")
        self._tinyurl = kwargs.get("tinyurl")
        self._maxsms = kwargs.get("maxsms")

    @property
    def format(self) -> str:
        """Format of the message. Default is SMS Message."""
        return self._format

    @property
    def text(self) -> str:
        """Text of the message."""
        return self._text

    def encode(self) -> Dict[str, Any]:
        """Message parameters in dict, prepared for the API."""
        res = {"mes": self._text}  # type: Dict[str, Any]
        if self._format is not None and self._format != "":
            res[self._format] = 1
        if self._translit is not None:
            res["translit"] = self._translit
        if self._tinyurl is not None:
            res["tinyurl"] = self._tinyurl
        if self._maxsms is not None:
            res["maxsms"] = self._maxsms
        return res

    def __str__(self) -> str:
        """Represent object as string."""
        return "<%s text=%s format=%s>" % (self.__class__.__name__, self._text, self._format)

    def __repr__(self) -> str:
        """Represent object for debug purposes."""
        return str(self)


class SMSMessage(Message):
    """
    SMS message type.

    :param str text: Text of the message
    :param dict kwargs: Dictionary for optional API parameters

    Usage::

        >>> from smsc import SMSMessage

        >>> m = SMSMessage(text="Hello, World!")
        >>> m
        <SMSMessage text=Hello, World! format=None>
    """

    def __init__(self, text: str, **kwargs: dict) -> None:  # noqa: D102
        assert len(text) <= 800
        super().__init__(text, msg_format=None, **kwargs)


class FlashMessage(Message):
    """
    Flash-SMS message type.

    :param str text: Text of the message
    :param dict kwargs: Dictionary for optional API parameters

    Usage::

        >>> from smsc import FlashMessage
        >>> m = FlashMessage(text="Hello, World!")
        >>> m
        <FlashMessage text=Hello, World! format=flash>
    """

    def __init__(self, text: str, **kwargs: dict) -> None:  # noqa: D102
        assert len(text) <= 800
        super().__init__(text, msg_format="flash", **kwargs)


class ViberMessage(Message):
    """
    Viber messenger message type.

    Note: Seems currently not working now.

    :param str text: Text of the message
    :param dict kwargs: Dictionary for optional API parameters

    Usage::

        >>> from smsc import ViberMessage
        >>> m = ViberMessage(text="Hello, World!")
        >>> m
        <ViberMessage text=Hello, World! format=viber>
    """

    def __init__(self, text: str, **kwargs: dict) -> None:  # noqa: D102
        assert len(text) <= 800
        super().__init__(text, msg_format="viber", **kwargs)
