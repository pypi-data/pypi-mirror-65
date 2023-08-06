"""
Main interface for meteringmarketplace service type definitions.

Usage::

    from mypy_boto3.meteringmarketplace.type_defs import UsageRecordTypeDef

    data: UsageRecordTypeDef = {...}
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
    "UsageRecordTypeDef",
    "UsageRecordResultTypeDef",
    "BatchMeterUsageResultTypeDef",
    "MeterUsageResultTypeDef",
    "RegisterUsageResultTypeDef",
    "ResolveCustomerResultTypeDef",
)

_RequiredUsageRecordTypeDef = TypedDict(
    "_RequiredUsageRecordTypeDef",
    {"Timestamp": datetime, "CustomerIdentifier": str, "Dimension": str},
)
_OptionalUsageRecordTypeDef = TypedDict(
    "_OptionalUsageRecordTypeDef", {"Quantity": int}, total=False
)


class UsageRecordTypeDef(_RequiredUsageRecordTypeDef, _OptionalUsageRecordTypeDef):
    pass


UsageRecordResultTypeDef = TypedDict(
    "UsageRecordResultTypeDef",
    {
        "UsageRecord": UsageRecordTypeDef,
        "MeteringRecordId": str,
        "Status": Literal["Success", "CustomerNotSubscribed", "DuplicateRecord"],
    },
    total=False,
)

BatchMeterUsageResultTypeDef = TypedDict(
    "BatchMeterUsageResultTypeDef",
    {"Results": List[UsageRecordResultTypeDef], "UnprocessedRecords": List[UsageRecordTypeDef]},
    total=False,
)

MeterUsageResultTypeDef = TypedDict(
    "MeterUsageResultTypeDef", {"MeteringRecordId": str}, total=False
)

RegisterUsageResultTypeDef = TypedDict(
    "RegisterUsageResultTypeDef",
    {"PublicKeyRotationTimestamp": datetime, "Signature": str},
    total=False,
)

ResolveCustomerResultTypeDef = TypedDict(
    "ResolveCustomerResultTypeDef", {"CustomerIdentifier": str, "ProductCode": str}, total=False
)
