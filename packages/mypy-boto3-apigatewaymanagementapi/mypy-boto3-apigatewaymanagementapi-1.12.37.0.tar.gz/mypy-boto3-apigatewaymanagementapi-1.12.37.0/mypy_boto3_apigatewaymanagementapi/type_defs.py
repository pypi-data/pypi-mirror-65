"""
Main interface for apigatewaymanagementapi service type definitions.

Usage::

    from mypy_boto3.apigatewaymanagementapi.type_defs import IdentityTypeDef

    data: IdentityTypeDef = {...}
"""
from datetime import datetime
import sys

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = ("IdentityTypeDef", "GetConnectionResponseTypeDef")

IdentityTypeDef = TypedDict("IdentityTypeDef", {"SourceIp": str, "UserAgent": str})

GetConnectionResponseTypeDef = TypedDict(
    "GetConnectionResponseTypeDef",
    {"ConnectedAt": datetime, "Identity": IdentityTypeDef, "LastActiveAt": datetime},
    total=False,
)
