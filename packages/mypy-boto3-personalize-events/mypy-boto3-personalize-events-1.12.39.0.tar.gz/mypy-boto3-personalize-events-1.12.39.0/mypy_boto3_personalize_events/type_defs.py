"""
Main interface for personalize-events service type definitions.

Usage::

    from mypy_boto3.personalize_events.type_defs import EventTypeDef

    data: EventTypeDef = {...}
"""
from datetime import datetime
import sys

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = ("EventTypeDef",)

_RequiredEventTypeDef = TypedDict(
    "_RequiredEventTypeDef", {"eventType": str, "properties": str, "sentAt": datetime}
)
_OptionalEventTypeDef = TypedDict("_OptionalEventTypeDef", {"eventId": str}, total=False)


class EventTypeDef(_RequiredEventTypeDef, _OptionalEventTypeDef):
    pass
