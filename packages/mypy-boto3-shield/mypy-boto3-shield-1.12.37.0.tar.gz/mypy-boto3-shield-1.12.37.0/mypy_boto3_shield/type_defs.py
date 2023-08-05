"""
Main interface for shield service type definitions.

Usage::

    from mypy_boto3.shield.type_defs import CreateProtectionResponseTypeDef

    data: CreateProtectionResponseTypeDef = {...}
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
    "CreateProtectionResponseTypeDef",
    "ContributorTypeDef",
    "AttackPropertyTypeDef",
    "MitigationTypeDef",
    "SummarizedCounterTypeDef",
    "SummarizedAttackVectorTypeDef",
    "SubResourceSummaryTypeDef",
    "AttackDetailTypeDef",
    "DescribeAttackResponseTypeDef",
    "DescribeDRTAccessResponseTypeDef",
    "EmergencyContactTypeDef",
    "DescribeEmergencyContactSettingsResponseTypeDef",
    "ProtectionTypeDef",
    "DescribeProtectionResponseTypeDef",
    "LimitTypeDef",
    "SubscriptionTypeDef",
    "DescribeSubscriptionResponseTypeDef",
    "GetSubscriptionStateResponseTypeDef",
    "AttackVectorDescriptionTypeDef",
    "AttackSummaryTypeDef",
    "ListAttacksResponseTypeDef",
    "ListProtectionsResponseTypeDef",
    "PaginatorConfigTypeDef",
    "TimeRangeTypeDef",
)

CreateProtectionResponseTypeDef = TypedDict(
    "CreateProtectionResponseTypeDef", {"ProtectionId": str}, total=False
)

ContributorTypeDef = TypedDict("ContributorTypeDef", {"Name": str, "Value": int}, total=False)

AttackPropertyTypeDef = TypedDict(
    "AttackPropertyTypeDef",
    {
        "AttackLayer": Literal["NETWORK", "APPLICATION"],
        "AttackPropertyIdentifier": Literal[
            "DESTINATION_URL",
            "REFERRER",
            "SOURCE_ASN",
            "SOURCE_COUNTRY",
            "SOURCE_IP_ADDRESS",
            "SOURCE_USER_AGENT",
            "WORDPRESS_PINGBACK_REFLECTOR",
            "WORDPRESS_PINGBACK_SOURCE",
        ],
        "TopContributors": List[ContributorTypeDef],
        "Unit": Literal["BITS", "BYTES", "PACKETS", "REQUESTS"],
        "Total": int,
    },
    total=False,
)

MitigationTypeDef = TypedDict("MitigationTypeDef", {"MitigationName": str}, total=False)

SummarizedCounterTypeDef = TypedDict(
    "SummarizedCounterTypeDef",
    {"Name": str, "Max": float, "Average": float, "Sum": float, "N": int, "Unit": str},
    total=False,
)

_RequiredSummarizedAttackVectorTypeDef = TypedDict(
    "_RequiredSummarizedAttackVectorTypeDef", {"VectorType": str}
)
_OptionalSummarizedAttackVectorTypeDef = TypedDict(
    "_OptionalSummarizedAttackVectorTypeDef",
    {"VectorCounters": List[SummarizedCounterTypeDef]},
    total=False,
)


class SummarizedAttackVectorTypeDef(
    _RequiredSummarizedAttackVectorTypeDef, _OptionalSummarizedAttackVectorTypeDef
):
    pass


SubResourceSummaryTypeDef = TypedDict(
    "SubResourceSummaryTypeDef",
    {
        "Type": Literal["IP", "URL"],
        "Id": str,
        "AttackVectors": List[SummarizedAttackVectorTypeDef],
        "Counters": List[SummarizedCounterTypeDef],
    },
    total=False,
)

AttackDetailTypeDef = TypedDict(
    "AttackDetailTypeDef",
    {
        "AttackId": str,
        "ResourceArn": str,
        "SubResources": List[SubResourceSummaryTypeDef],
        "StartTime": datetime,
        "EndTime": datetime,
        "AttackCounters": List[SummarizedCounterTypeDef],
        "AttackProperties": List[AttackPropertyTypeDef],
        "Mitigations": List[MitigationTypeDef],
    },
    total=False,
)

DescribeAttackResponseTypeDef = TypedDict(
    "DescribeAttackResponseTypeDef", {"Attack": AttackDetailTypeDef}, total=False
)

DescribeDRTAccessResponseTypeDef = TypedDict(
    "DescribeDRTAccessResponseTypeDef", {"RoleArn": str, "LogBucketList": List[str]}, total=False
)

EmergencyContactTypeDef = TypedDict("EmergencyContactTypeDef", {"EmailAddress": str})

DescribeEmergencyContactSettingsResponseTypeDef = TypedDict(
    "DescribeEmergencyContactSettingsResponseTypeDef",
    {"EmergencyContactList": List[EmergencyContactTypeDef]},
    total=False,
)

ProtectionTypeDef = TypedDict(
    "ProtectionTypeDef",
    {"Id": str, "Name": str, "ResourceArn": str, "HealthCheckIds": List[str]},
    total=False,
)

DescribeProtectionResponseTypeDef = TypedDict(
    "DescribeProtectionResponseTypeDef", {"Protection": ProtectionTypeDef}, total=False
)

LimitTypeDef = TypedDict("LimitTypeDef", {"Type": str, "Max": int}, total=False)

SubscriptionTypeDef = TypedDict(
    "SubscriptionTypeDef",
    {
        "StartTime": datetime,
        "EndTime": datetime,
        "TimeCommitmentInSeconds": int,
        "AutoRenew": Literal["ENABLED", "DISABLED"],
        "Limits": List[LimitTypeDef],
    },
    total=False,
)

DescribeSubscriptionResponseTypeDef = TypedDict(
    "DescribeSubscriptionResponseTypeDef", {"Subscription": SubscriptionTypeDef}, total=False
)

GetSubscriptionStateResponseTypeDef = TypedDict(
    "GetSubscriptionStateResponseTypeDef", {"SubscriptionState": Literal["ACTIVE", "INACTIVE"]}
)

AttackVectorDescriptionTypeDef = TypedDict("AttackVectorDescriptionTypeDef", {"VectorType": str})

AttackSummaryTypeDef = TypedDict(
    "AttackSummaryTypeDef",
    {
        "AttackId": str,
        "ResourceArn": str,
        "StartTime": datetime,
        "EndTime": datetime,
        "AttackVectors": List[AttackVectorDescriptionTypeDef],
    },
    total=False,
)

ListAttacksResponseTypeDef = TypedDict(
    "ListAttacksResponseTypeDef",
    {"AttackSummaries": List[AttackSummaryTypeDef], "NextToken": str},
    total=False,
)

ListProtectionsResponseTypeDef = TypedDict(
    "ListProtectionsResponseTypeDef",
    {"Protections": List[ProtectionTypeDef], "NextToken": str},
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

TimeRangeTypeDef = TypedDict(
    "TimeRangeTypeDef", {"FromInclusive": datetime, "ToExclusive": datetime}, total=False
)
