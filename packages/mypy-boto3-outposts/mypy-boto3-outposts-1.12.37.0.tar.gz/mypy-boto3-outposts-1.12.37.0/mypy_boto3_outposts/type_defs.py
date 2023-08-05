"""
Main interface for outposts service type definitions.

Usage::

    from mypy_boto3.outposts.type_defs import OutpostTypeDef

    data: OutpostTypeDef = {...}
"""
import sys
from typing import List

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "OutpostTypeDef",
    "CreateOutpostOutputTypeDef",
    "InstanceTypeItemTypeDef",
    "GetOutpostInstanceTypesOutputTypeDef",
    "GetOutpostOutputTypeDef",
    "ListOutpostsOutputTypeDef",
    "SiteTypeDef",
    "ListSitesOutputTypeDef",
)

OutpostTypeDef = TypedDict(
    "OutpostTypeDef",
    {
        "OutpostId": str,
        "OwnerId": str,
        "OutpostArn": str,
        "SiteId": str,
        "Name": str,
        "Description": str,
        "LifeCycleStatus": str,
        "AvailabilityZone": str,
        "AvailabilityZoneId": str,
    },
    total=False,
)

CreateOutpostOutputTypeDef = TypedDict(
    "CreateOutpostOutputTypeDef", {"Outpost": OutpostTypeDef}, total=False
)

InstanceTypeItemTypeDef = TypedDict("InstanceTypeItemTypeDef", {"InstanceType": str}, total=False)

GetOutpostInstanceTypesOutputTypeDef = TypedDict(
    "GetOutpostInstanceTypesOutputTypeDef",
    {
        "InstanceTypes": List[InstanceTypeItemTypeDef],
        "NextToken": str,
        "OutpostId": str,
        "OutpostArn": str,
    },
    total=False,
)

GetOutpostOutputTypeDef = TypedDict(
    "GetOutpostOutputTypeDef", {"Outpost": OutpostTypeDef}, total=False
)

ListOutpostsOutputTypeDef = TypedDict(
    "ListOutpostsOutputTypeDef", {"Outposts": List[OutpostTypeDef], "NextToken": str}, total=False
)

SiteTypeDef = TypedDict(
    "SiteTypeDef", {"SiteId": str, "AccountId": str, "Name": str, "Description": str}, total=False
)

ListSitesOutputTypeDef = TypedDict(
    "ListSitesOutputTypeDef", {"Sites": List[SiteTypeDef], "NextToken": str}, total=False
)
