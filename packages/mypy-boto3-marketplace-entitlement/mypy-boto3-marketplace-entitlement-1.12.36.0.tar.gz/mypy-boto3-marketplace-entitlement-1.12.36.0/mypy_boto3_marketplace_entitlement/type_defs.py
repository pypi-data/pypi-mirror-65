"""
Main interface for marketplace-entitlement service type definitions.

Usage::

    from mypy_boto3.marketplace_entitlement.type_defs import EntitlementValueTypeDef

    data: EntitlementValueTypeDef = {...}
"""
from datetime import datetime
import sys
from typing import List

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "EntitlementValueTypeDef",
    "EntitlementTypeDef",
    "GetEntitlementsResultTypeDef",
    "PaginatorConfigTypeDef",
)

EntitlementValueTypeDef = TypedDict(
    "EntitlementValueTypeDef",
    {"IntegerValue": int, "DoubleValue": float, "BooleanValue": bool, "StringValue": str},
    total=False,
)

EntitlementTypeDef = TypedDict(
    "EntitlementTypeDef",
    {
        "ProductCode": str,
        "Dimension": str,
        "CustomerIdentifier": str,
        "Value": EntitlementValueTypeDef,
        "ExpirationDate": datetime,
    },
    total=False,
)

GetEntitlementsResultTypeDef = TypedDict(
    "GetEntitlementsResultTypeDef",
    {"Entitlements": List[EntitlementTypeDef], "NextToken": str},
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)
