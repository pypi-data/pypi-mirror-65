"""
Main interface for iotsecuretunneling service type definitions.

Usage::

    from mypy_boto3.iotsecuretunneling.type_defs import ConnectionStateTypeDef

    data: ConnectionStateTypeDef = {...}
"""
from datetime import datetime
import sys
from typing import List

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ConnectionStateTypeDef",
    "DestinationConfigTypeDef",
    "TagTypeDef",
    "TimeoutConfigTypeDef",
    "TunnelTypeDef",
    "DescribeTunnelResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TunnelSummaryTypeDef",
    "ListTunnelsResponseTypeDef",
    "OpenTunnelResponseTypeDef",
)

ConnectionStateTypeDef = TypedDict(
    "ConnectionStateTypeDef",
    {"status": Literal["CONNECTED", "DISCONNECTED"], "lastUpdatedAt": datetime},
    total=False,
)

DestinationConfigTypeDef = TypedDict(
    "DestinationConfigTypeDef", {"thingName": str, "services": List[str]}
)

TagTypeDef = TypedDict("TagTypeDef", {"key": str, "value": str})

TimeoutConfigTypeDef = TypedDict(
    "TimeoutConfigTypeDef", {"maxLifetimeTimeoutMinutes": int}, total=False
)

TunnelTypeDef = TypedDict(
    "TunnelTypeDef",
    {
        "tunnelId": str,
        "tunnelArn": str,
        "status": Literal["OPEN", "CLOSED"],
        "sourceConnectionState": ConnectionStateTypeDef,
        "destinationConnectionState": ConnectionStateTypeDef,
        "description": str,
        "destinationConfig": DestinationConfigTypeDef,
        "timeoutConfig": TimeoutConfigTypeDef,
        "tags": List[TagTypeDef],
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
    },
    total=False,
)

DescribeTunnelResponseTypeDef = TypedDict(
    "DescribeTunnelResponseTypeDef", {"tunnel": TunnelTypeDef}, total=False
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"tags": List[TagTypeDef]}, total=False
)

TunnelSummaryTypeDef = TypedDict(
    "TunnelSummaryTypeDef",
    {
        "tunnelId": str,
        "tunnelArn": str,
        "status": Literal["OPEN", "CLOSED"],
        "description": str,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
    },
    total=False,
)

ListTunnelsResponseTypeDef = TypedDict(
    "ListTunnelsResponseTypeDef",
    {"tunnelSummaries": List[TunnelSummaryTypeDef], "nextToken": str},
    total=False,
)

OpenTunnelResponseTypeDef = TypedDict(
    "OpenTunnelResponseTypeDef",
    {"tunnelId": str, "tunnelArn": str, "sourceAccessToken": str, "destinationAccessToken": str},
    total=False,
)
