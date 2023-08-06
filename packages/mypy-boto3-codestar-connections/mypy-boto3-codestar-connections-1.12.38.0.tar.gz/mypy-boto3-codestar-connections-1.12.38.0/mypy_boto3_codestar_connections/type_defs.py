"""
Main interface for codestar-connections service type definitions.

Usage::

    from mypy_boto3.codestar_connections.type_defs import CreateConnectionOutputTypeDef

    data: CreateConnectionOutputTypeDef = {...}
"""
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
    "CreateConnectionOutputTypeDef",
    "ConnectionTypeDef",
    "GetConnectionOutputTypeDef",
    "ListConnectionsOutputTypeDef",
)

CreateConnectionOutputTypeDef = TypedDict("CreateConnectionOutputTypeDef", {"ConnectionArn": str})

ConnectionTypeDef = TypedDict(
    "ConnectionTypeDef",
    {
        "ConnectionName": str,
        "ConnectionArn": str,
        "ProviderType": Literal["Bitbucket"],
        "OwnerAccountId": str,
        "ConnectionStatus": Literal["PENDING", "AVAILABLE", "ERROR"],
    },
    total=False,
)

GetConnectionOutputTypeDef = TypedDict(
    "GetConnectionOutputTypeDef", {"Connection": ConnectionTypeDef}, total=False
)

ListConnectionsOutputTypeDef = TypedDict(
    "ListConnectionsOutputTypeDef",
    {"Connections": List[ConnectionTypeDef], "NextToken": str},
    total=False,
)
